from django.shortcuts import redirect, render
from .forms import Code_register_form, Phone_login_form, Register, password_login_form,code_login_form,Phone_register_form
from .models import Address, Code,Sign_up, User_detail
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib import messages
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
import pytz
import re
import datetime
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.models import User
# Create your views here.
 

def login2(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request,'loginv2.html',{})


def contact_us(request):
    return render(request,'contact_us.html',{})


def about_us(request):
    return render(request,'about_us.html',{})




################################# login APIS ###########################################


class Resend(APIView):
    def post(self, request):
        phone=request.data.get('phone')
        user=User.objects.filter(username=phone).first()
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

        return Response(status=status.HTTP_200_OK)
        
class Check_The_Code(APIView):
    
    def post(self, request):
        phone=request.data.get('phone')
        code=request.data.get('code')
        user=User.objects.filter(username=phone).first()
        expired_time=user.code.expired_time.astimezone(timezone.get_current_timezone())
        print(expired_time)
        if user.code.code==code and expired_time>=timezone.now():
            login(request,user)
            return Response({'address':'http://127.0.0.1:8000'},status=status.HTTP_200_OK)
        else:
            return Response({'code_error':'کد منتقضی شده یا نادرست است'},status=status.HTTP_400_BAD_REQUEST)
            

class Send_The_Code(APIView):
    
    def post(self, request):
        phone=request.data.get('phone')
        user=User.objects.filter(username=phone).first()
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
        html=f""" 
             <div class="form-inline" id="login-form"  >
                            <p class="text-right text-info">رمز پیامکی  به شماره تلفن {phone} ارسال شد  </p>
                            <label for="phone" class="text-info mt-2">کد پیامکی : </label><br>
                            <div class="input-group form-group">
                                <input type="text" onKeyDown="if(event.keyCode==13) check_the_code();" name="code" id="code" class="form-control" placeholder="کد تایید" required="">                                      
                                <div class="input-group-prepend ">
                                     <button class="btn btn-info btn-md " style="height:46px;" onclick="check_the_code()">ادامه</button>
                                </div>
                            </div>
                             <span class="text-danger" id="error" style="display:none;"></span><br>
                        
                            <p id="link">  ارسال مجدد کد در <span id='time'> (04:00) </span></p>  
                           
                        </div>
                        <div id="register-link" class="text-right">
                            <a href="javascript:void(0)" onclick='by_pass()' class="text-info ">ورود با رمز عبور</a>
                        </div>
        """ 
        return Response({'html':html},status=status.HTTP_200_OK)


class Check_Password(APIView):
    
    def post(self, request):
        phone=request.data.get('phone')
        password=request.data.get('password')
        user=User.objects.filter(username=phone).first()
        if user.check_password(password):
            login(request,user)
            return Response({'address':'http://127.0.0.1:8000'},status=status.HTTP_200_OK)
        return Response({'password_error':'گذرواژه درست نیست '},status=status.HTTP_400_BAD_REQUEST)
        
class Check_Phone(APIView):
    
    def post(self, request):
        phone=request.data.get('phone')
        if re.search(r"^09\d{9}$",phone) is None:
            return Response({'phone_error':'شماره تلفن اشتباست'},status=status.HTTP_400_BAD_REQUEST)
        user=User.objects.filter(username=phone)
        if user.exists():
            html="""  
                     <div class="form-inline" id="login-form">
                        <p class="text-right text-info">رمز خود را وارد کنید </p>
                        <label for="phone" class="text-info mt-2">پسورد : </label><br>
                        <div class="input-group form-group">
                            <input type="text" onKeyDown="if(event.keyCode==13) send_password();" name="password" id="password" class="form-control" placeholder="رمز عبور" required="">                                       
                            <div class="input-group-prepend ">
                                <button class="btn btn-info btn-md " style="height:46px;" onclick="send_password()">ادامه</button>
                            </div>
                        </div>
                         <span class="text-danger" id="error" style="display:none;"></span>
                    </div>

                    <div id="register-link" class="text-right">
                                            <a href="javascript:void" class="text-info " onclick="send_code()">ورود با رمز عبور پیامکی </a>
                    </div>
            """
            return Response({'phone':phone,'password':html},status=status.HTTP_200_OK)
        else:
            return Response({'phone_error':'شماره تلفن موجود نیست '},status=status.HTTP_400_BAD_REQUEST)
            







################################# /login APIS ###########################################









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

            

        


def log_out(request):
    logout(request)
    return redirect('/')

