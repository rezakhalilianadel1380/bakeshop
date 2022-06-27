from email import message
from random import random
from django.shortcuts import redirect, render
from .forms import Code_register_form, Phone_login_form, Register, password_login_form,code_login_form,Phone_register_form
from .models import Address, Code,Sign_up, User_detail
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib import messages
import datetime
import uuid
import pytz
# Create your views here.
 
 
def contact_us(request):
    return render(request,'contact_us.html',{})

def about_us(request):
    return render(request,'about_us.html',{})





















def sign_up(request):
    if request.user.is_authenticated:
        return redirect('/')
    form=Phone_register_form(request.POST or None)
    if form.is_valid():
        phone_number=form.cleaned_data.get('phone')
        phone_object=User_detail.objects.filter(phone_number=phone_number)
        if phone_object.exists():
            form.add_error('phone','تلفن در سیستم ثبت شده است ')
        else:
            request.session['phone_number_sign_code']=phone_number
            return redirect('signup/code')
    context={
        'form':form,
    }
    return render(request,'sign_up.html',context)

def sign_up_code(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.session.get('phone_number_sign_code') is not None:
        phone_number=request.session.get('phone_number_sign_code')
        if request.method=='GET':
                code=Sign_up.objects.filter(phone_number=phone_number)
                if code.exists():
                    code=code.first()
                    code.expired_time=datetime.datetime.now()+datetime.timedelta(minutes=4)
                    code.code=str(uuid.uuid4().int)[:6]
                    code.save()
                    print(code.code)
                else:
                    code=Sign_up.objects.create(phone_number=phone_number,expired_time=datetime.datetime.now()+datetime.timedelta(minutes=4))
                    code.code=str(uuid.uuid4().int)[:6]
                    code.save()
                    print(code.code)

        form=Code_register_form(request.POST or None)
        if form.is_valid():
            code=form.cleaned_data.get('codes')
            code_object=Sign_up.objects.filter(phone_number=phone_number,code=code)
            utc=pytz.UTC
            current_time= utc.localize(datetime.datetime.now()) 
            if code_object.exists() and  code_object.first().expired_time>current_time:
                request.session['checked']=True
                return redirect('register')
            else:
                form.add_error('codes','کد وارد شده اشتباه است')
        context={
            'form':form,
        }
        return render(request,'sign_up_code.html',context)
    else:
        return redirect("/sign_up")

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.session.get('checked') is not None and request.session.get('checked')==True:
        phone_number=request.session['phone_number_sign_code']
        form=Register(request.POST or None)
        if form.is_valid():
            name=form.cleaned_data.get('name')
            family=form.cleaned_data.get('family')
            address=form.cleaned_data.get('address')
            password=form.cleaned_data.get('password')
            user=User.objects.create_user(username=phone_number,password=password,first_name=name,last_name=family)
            user_detail=User_detail.objects.create(user=user,phone_number=phone_number)
            Address.objects.create(user=user,address=address)
            del request.session['checked']
            del request.session['phone_number_sign_code']
            return redirect ('/login')
        context={
            'form':form,
        }
        return render(request,'register.html',context)
    else:
        return redirect('/signup')

            

        




def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    form=Phone_login_form(request.POST or None)
    if form.is_valid():
        phone_number=form.cleaned_data.get('phone')
        phone_object=User_detail.objects.filter(phone_number=phone_number)
        if phone_object.exists():
            request.session['user_id']=phone_object.first().user.id
            request.session['phone_number']=phone_object.first().phone_number
            return redirect('login/password')
        else:
            form.add_error('phone','تلفن در سیستم ثبت نشده است ')
    context={
        'form':form,
    }
    return render(request,'login.html',context)

def log_out(request):
    logout(request)
    return redirect('/')

def login_password(request):
    if request.user.is_authenticated:
        return redirect('/')
    form=password_login_form(request.POST or None)
    if request.session.get('user_id') is not None:
        if form.is_valid():
            password=form.cleaned_data.get('password')
            user_id=request.session.get('user_id')
            phone_number=request.session.get('phone_number')
            user=User.objects.get(id=user_id)
            if user.check_password(password):
                login(request,user)
                del request.session['user_id']
                del request.session['phone_number']
                return redirect('/')
            else:
                form.add_error('password','رمز عبور اشتباه است')
        
        context={
            'form':form,
        }
        return render(request,'login_password.html',context)
    else:
        return redirect('/login')


def login_code(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.session.get('user_id') is not None:
        if request.method=='GET':
            user=User.objects.get(id=request.session.get('user_id'))
            code=Code.objects.filter(user=user)
            if code.exists():
                code=code.first()
                code.expired_time=datetime.datetime.now()+datetime.timedelta(minutes=4)
                code.code=str(uuid.uuid4().int)[:6]
                code.save()
                print(code.code)
            else:
                code=Code.objects.create(user=user,expired_time=datetime.datetime.now()+datetime.timedelta(minutes=4))
                code.code=str(uuid.uuid4().int)[:6]
                code.save()
                print(code.code)
                
        form=code_login_form(request.POST or None)
        if form.is_valid():
            code=form.cleaned_data.get('code')
            user_id=request.session.get('user_id')
            phone_number=request.session.get('phone_number')
            user=User.objects.get(id=user_id)
            utc=pytz.UTC
            current_time= utc.localize(datetime.datetime.now()) 
            if user.code.code==code and user.code.expired_time>=current_time:
                login(request,user)
                del request.session['user_id']
                del request.session['phone_number']
                messages.success(request,'شما با موفقیت وارد شدید')
                return redirect('/')
            else:
                form.add_error('code','کد تایید اشتباست یا منقضی شده است')

        context={
                'form':form,
            }
        return render(request,'login_code.html',context)
    else:
        return redirect('/login')

 