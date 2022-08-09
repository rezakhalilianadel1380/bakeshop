from django.shortcuts import redirect, render
from .models import Code,Sign_up, User_detail
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
import re
import random
import datetime
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.models import User
from shop.settings import LOGIN_URL
# Create your views here.
 

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
        code.expired_time=datetime.datetime.now()+datetime.timedelta(minutes=4)
        code.code=random.randint(1000,9999)
        code.save()
        print(code.save)
        return Response(status=status.HTTP_200_OK)
        

class Check_The_Code(APIView):
    def post(self, request):
        phone=request.data.get('phone')
        code=request.data.get('code')
        user=User.objects.filter(username=phone).first()
        expired_time=user.code.expired_time.astimezone(timezone.get_current_timezone())
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
        if not code.exists():
            code=Code.objects.create(user=user)
        else:
            code=code.first()
        code.expired_time=datetime.datetime.now()+datetime.timedelta(minutes=4)
        code.code=random.randint(1000,9999)
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
        code.expired_time=datetime.datetime.now()+datetime.timedelta(minutes=4)
        code.save()
        print(code.code)
        return Response(status=status.HTTP_200_OK)



class Register_User(APIView):
    def post(self,request):
        firstname=request.data.get('firstname')
        lastname=request.data.get('lastname')
        password=request.data.get('password')
        re_password=request.data.get('re_password')
        phone=request.COOKIES.get('phonenumber')
        user:User=User.objects.filter(username=phone).first()
        user.first_name=firstname
        user.last_name=lastname
        user.set_password(password)
        user.is_active=True
        user.save()
        return Response({'address':f'http://127.0.0.1:8000{LOGIN_URL}'},status=status.HTTP_200_OK)


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
            html=f"""
                      <div class="form-inline" id="login-form" >
                        <p class="text-right text-info">فرم ثبت نام </p>

                        <div class="form-group">
                            <label for="firstname" class="text-info mt-2">نام :</label><br>
                            <input type="text" id="firstname"  class="form-control"  placeholder="نام ">                                   
                        </div>
                        <div class="form-group">
                            <label for="family" class="text-info mt-2">نام و خانوادگی :</label><br>
                            <input type="text" id="lastname" class="form-control"  placeholder="نام خانوادگی">
                                   
                        </div>
                        <div class="form-group">
                            <label for="password" class="text-info mt-2">پسورد :</label><br>
                            <input type="text" id="password"  class="form-control"  placeholder="رمز عبور">
                        </div>
                        <div class="form-group">
                            <label for="re_password" class="text-info mt-2">تکرار رمز عبور :</label><br>
                           <input type="text" id="re_password"  class="form-control"  placeholder="تکرار رمز عبور">
                        </div>
                        <br>
                        <button onclick='send_information()' class="btn btn-info w-100">ثبت نام</button>
                    </div>
                """
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
        code.expired_time=datetime.datetime.now()+datetime.timedelta(minutes=4)
        code.save()
        print(code.code)
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
