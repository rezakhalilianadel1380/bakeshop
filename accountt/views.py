from django.contrib import messages
from django.shortcuts import redirect, render
from order.models import Cart
from .models import Address, Code,Sign_up, User_detail
from .forms import Register,User_Form,User_Address
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from rest_framework.views import APIView
from rest_framework.response import Response
import re
import random
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.models import User
from shop.settings import LOGIN_URL
from django.template.loader import render_to_string
from sms_configure.sms import send_message
from django.contrib.auth.decorators import login_required
# Create your views here.


def delete_address(request,id):
    instance=Address.objects.filter(user=request.user,id=id)
    if not instance.exists():
        return redirect('/profile/Address')
    instance.delete()
    messages.success(request,'ادرس  با موفقیت حذف  شد ')
    return redirect('/profile/Address')



@login_required
def edite_address(request,id):
    instance=Address.objects.filter(user=request.user,id=id)
    if not instance.exists():
        return redirect('/profile/Address')
    form=User_Address(request.POST or None,instance=instance.first())
    if form.is_valid():
        messages.success(request,'ادرس  با موفقیت ویرایش شد ')
        form.save()
        return redirect('/profile/Address')
    context={
        'form':form,
    }
    return render(request,'edite_address.html',context)

@login_required
def add_address(request):
    address=Address.objects.filter(user=request.user)
    if len(address)>=3:
        messages.error(request,'داشتن بیش از سه ادرس مجاز نیست')
        return redirect('/profile/Address')
    form=User_Address(request.POST or None)
    if form.is_valid():
        messages.success(request,'ادرس  با موفقیت ایجاد شد ')
        add=form.save(commit=False)
        add.user=request.user
        add.save()
        return redirect('/profile/Address')
    context={
        'form':form,
    }
    return render(request,'add_address.html',context)


@login_required
def show_addresses_in_profile(request):
    return render(request,'address.html',{})


@login_required
def show_orders_profile(request):
    orders=Cart.objects.filter(user=request.user,status__in=['4','5'])
    active_order=Cart.objects.filter(user=request.user,status__in=['2','3'])
    context={
        "orders":orders,
        'active_order':active_order,
    }
    return render(request,'order_profile.html',context)


def show_right_panel(request):
    return render(request,'right_panel.html',{})

@login_required
def edite_account(request):
    form=User_Form(request.POST or None,instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request,'حساب کاربری با موفقیت ویرایش شد ')
        return redirect('/profile/EditeProfile')
    context={
        'form':form,
    }
    return render(request,'edite_account.html',context)

@login_required
def profile_dashbord(request):
    return render(request,'profile.html',{})

def log_out(request):
    logout(request)
    return redirect('/')


def contact_us(request):
    return render(request,'contact_us.html',{})


def about_us(request):
    return render(request,'about_us.html',{})




################################# login  ###########################################


def login2(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request,'loginv2.html',{})


class Resend(APIView):
    def post(self, request):
        phone=request.data.get('phone')
        user=User.objects.filter(username=phone).first()
        code=Code.objects.filter(user=user)
        if not code.exists():
            code=Code.objects.create(user=user)
        else:
            code=code.first()
        code.expired_time=timezone.now()+timezone.timedelta(minutes=4)
        code.code=random.randint(1000,9999)
        code.save()
        message=f"""
        نانوی شاپ 
        سلام خوش اومدید 
        کد ورود شما  : {code.code}
        """
        send_message(phone,message)
        return Response(status=status.HTTP_200_OK)
        

class Check_The_Code(APIView):
    def post(self, request):
        phone=request.data.get('phone')
        code=request.data.get('code')
        user=User.objects.filter(username=phone).first()
        expired_time=user.code.expired_time.astimezone(timezone.get_current_timezone())
        current_time=timezone.now().astimezone(timezone.get_current_timezone())
        if user.code.code==code and expired_time>=current_time:
            login(request,user)
            return Response({'address':'http://127.0.0.1:8000'},status=status.HTTP_200_OK)
        else:
            return Response({'code_error':'کد منتقضی شده یا نادرست است'},status=status.HTTP_400_BAD_REQUEST)
            



class Send_The_Code(APIView):
    def post(self, request):
        phone=request.data.get('phone')
        user=User.objects.filter(username=phone).first()
        code=Code.objects.filter(user=user)
        if not code.exists():
            code=Code.objects.create(user=user)
        else:
            code=code.first()
        code.expired_time=timezone.now()+timezone.timedelta(minutes=4)
        code.code=random.randint(1000,9999)
        code.save()
        message=f"""
        نانوی شاپ 
        سلام خوش اومدید 
        کد ورود شما  : {code.code}
        """
        send_message(phone,message)
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
        user=User.objects.filter(username=phone,is_active=True)
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
            


################################# /login  ###########################################




################################## sign up  ##############################################

def sign_upv2(request):
    return render(request,'sign_upv2.html',{})

class Resend_Code(APIView):
    def get(self,request):
        phone=request.COOKIES.get('phonenumber')
        code=Sign_up.objects.filter(phone_number=phone)  
        if not code.exists():
            code=Sign_up.objects.create(phone_number=phone)
        else:
            code=code.first()
        code.code=random.randint(1000,9999)
        code.expired_time=timezone.now()+timezone.timedelta(minutes=4)
        code.save()
        message=f"""
        نانوی شاپ 
        سلام خوش اومدید 
        کد ثبت نام شما  : {code.code}
        """
        send_message(phone,message)
        return Response(status=status.HTTP_200_OK)

class Register_User(APIView):
    def post(self,request):
        phone=request.COOKIES.get('phonenumber')
        user:User=User.objects.filter(username=phone).first()
        form=Register(request.data or None)
        if form.is_valid():
            firstname=form.cleaned_data.get('first_name')
            lastname=form.cleaned_data.get('family')
            password=form.cleaned_data.get('password')
            user.first_name=firstname
            user.last_name=lastname
            user.set_password(password)
            user.is_active=True
            user.save()
            return Response({'address':f'http://127.0.0.1:8000{LOGIN_URL}'},status=status.HTTP_200_OK)
        context={
                'form':form
            }
        html=render_to_string('register_form.html',context)
        return Response({'html':html},status=status.HTTP_400_BAD_REQUEST)
        

class Check_Code_Sign_Up(APIView):
    def post(self, request):
        code=request.data.get('code')
        phone=request.COOKIES.get('phonenumber')
        code_object=Sign_up.objects.filter(phone_number=phone).first()
        expired_time=code_object.expired_time.astimezone(timezone.get_current_timezone())
        if code_object.code==code and expired_time>=timezone.now():
            if not User.objects.filter(username=phone).exists():
                user=User.objects.create(username=phone,is_active=False)
                User_detail.objects.create(user=user)
            form=Register()
            context={
                'form':form
            }
            html=render_to_string('register_form.html',context)
            return Response({'html':html},status=status.HTTP_200_OK)
        else:
            return Response({'code_error':'کد منتقضی شده یا نادرست است'},status=status.HTTP_400_BAD_REQUEST)
            
  

class Check_Phone_Sign_Up(APIView):
    def post(self, request):
        phone=request.data.get('phone')
        if re.search(r"^09\d{9}$",phone) is None:
            return Response({'phone_error':'شماره تلفن اشتباست'},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=phone,is_active=True).exists():
            return Response({'phone_error':'کاربر قبلا ثبت نام شده است '},status=status.HTTP_400_BAD_REQUEST)
        code=Sign_up.objects.filter(phone_number=phone)  
        if not code.exists():
            code=Sign_up.objects.create(phone_number=phone)
        else:
            code=code.first()
        code.code=random.randint(1000,9999)
        code.expired_time=timezone.now()+timezone.timedelta(minutes=4)
        code.save()
        message=f"""
        نانوی شاپ 
        سلام خوش اومدید 
        کد ثبت نام شما  : {code.code}
        """
        send_message(phone,message)
        html=f""" 
             <div class="form-inline" id="login-form"  >
                            <p class="text-right text-info">رمز پیامکی  به شماره تلفن {phone} ارسال شد  </p>
                            <label for="phone" class="text-info mt-2">کد پیامکی : </label><br>
                            <div class="input-group form-group">
                                <input type="text" onKeyDown="if(event.keyCode==13) send_code();" name="code" id="code" class="form-control" placeholder="کد تایید" required="">                                      
                                <div class="input-group-prepend ">
                                     <button class="btn btn-info btn-md " style="height:46px;" onclick="send_code()">ادامه</button>
                                </div>
                            </div>
                             <span class="text-danger" id="error" style="display:none;"></span><br>
                        
                            <p id="link">  ارسال مجدد کد در <span id='time'> (04:00) </span></p>  
                           
            </div>
        """   
        return Response({'html':html,'phone':phone},status=status.HTTP_200_OK)
            



################################## /sign up  ##############################################
