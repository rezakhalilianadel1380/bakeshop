from django.shortcuts import redirect, render
from bread.models import Bread
from order.models import Cart
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from accountt.models import Setting, User_detail
from rest_framework import status
from django.contrib import messages
from .forms import Bread_Form, User_Detail_Form,User_Form,login_form,Setting_edite_Form
from django.contrib.auth.password_validation import validate_password
import re
from django.core.exceptions import ValidationError,FieldError
import datetime
from django.db.models import Q
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout,authenticate,login
from accountt.models import Setting
from .permissions import Is_View_Cart,Read_Only,Bread_permission,Change_Cart_Permisson,Setting_Permission,User_Delete_Permission
from rest_framework import permissions
from sms_configure.sms import send_message
# from django.contrib.auth import mixins 
# from .serializers import Bread_Serializer
# from rest_framework.exceptions import PermissionDenied
# from rest_framework import generics
# from django.http import Http404
# Create your views here.




@user_passes_test(lambda u: u.has_perm('accountt.change_setting'),login_url='/adminlte/login')
def setting_edite(request,id):
    setting=Setting.objects.filter(id=1).first()
    form=Setting_edite_Form(request.POST or None,instance=setting)
    if form.is_valid():
        form.save()
        return redirect('/adminlte/setting')

    context={
        'form':form,
    }
    return render(request,'setting_edite.html',context)




@user_passes_test(lambda u: u.has_perm('accountt.view_setting'),login_url='/adminlte/login')
def setting_site(request):
    setting=Setting.objects.filter(id=1).first()
    context={
        'setting':setting
    }
    return render(request,'setting.html',context)




def admin_logout(request):
    logout(request)
    return redirect('/adminlte/login')


def admin_login(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('/adminlte')
    form=login_form(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_staff:
                login(request,user)
                next_page=request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('/adminlte')
            form.add_error('username','اجازه دسترسی داده نشد')
        else:
            form.add_error('username','کاربر یافت نشد ')
    context={
        'form':form
    }
    return render(request,'login_admin.html',context)




@user_passes_test(lambda u: u.is_superuser,login_url='/adminlte/login')
def show_orders(request):
    carts=Cart.objects.all().order_by('-payment_date')
    if request.GET.get('filter_time') and request.GET.get('filter_time')=='1' :
       carts=carts.filter(payment_date__day=timezone.now().day)
    elif  request.GET.get('filter_time') and request.GET.get('filter_time')=='2' :
       carts=carts.filter(payment_date__month=timezone.now().month)
    elif request.GET.get('filter_time') and request.GET.get('filter_time')=='3' :
       carts=carts.filter(payment_date__year=timezone.now().year)
    if request.GET.get('qs'):
        q=request.GET.get('qs')
        lookup=(
           Q(user__username=q)|
           Q(user__first_name__contains=q)|
           Q(user__last_name__contains=q)
        )
        carts=Cart.objects.filter(lookup).distinct()
    paginator = Paginator(carts,20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'page_obj':page_obj,
        'carts':carts
    }
    return render(request,"orders.html",context)







@user_passes_test(lambda u: u.has_perm('order.can_access_produce_section'),login_url='/adminlte/login')
def produce_bread(request):
    today = datetime.datetime.today()
    carts=Cart.objects.filter(payment_date__day=today.day)
    cart=Cart.objects.filter(status__in=['2',"3"]).first()
    context={
        'carts':carts,
        'cart':cart,
    }
    return render(request,'produce_bread.html',context)


@user_passes_test(lambda u: u.has_perm('auth.change_user'),login_url='/adminlte/login')
def edite_user(request,id):
    user=User.objects.filter(id=id).first()
    if user is None:
        messages.success(request,'کاربری یافت نشد شاید حذف شده باشد ')
        return redirect('/adminlte/users')
    user_detail=User_detail.objects.get(user=user)
    form=User_Form(request.POST or None,instance=user)
    form2=User_Detail_Form(request.POST or None,request.FILES or None,instance=user_detail)
    if form.is_valid() and form2.is_valid():
        form.save()
        form2.save()
        messages.success(request,'ویرایش شد ')
        return redirect('/adminlte/users')
    context={
        'form':form,
        'form2':form2,
    }
    return render(request,'user_edite.html',context)



def validate_username(username):
    if re.search(r"^09\d{9}$",username) is None:
        raise FieldError("شماره تلفن معتبر نیست ")
    else:
        return None


@user_passes_test(lambda u: u.has_perm('auth.add_user'),login_url='/adminlte/login')
def add_user(request):
    form=User_Form(request.POST or None)
    form2=User_Detail_Form(request.POST or None,request.FILES or None)
    if form.is_valid() and form2.is_valid():
        user=form.save(commit=False)
        password = form.cleaned_data.get('password')
        username = form.cleaned_data['username']
        try:
            validate_password(password,user)
            validate_username(username=username)
            user.set_password(password)
            user.save()
            user_detail=form2.save(commit=False)
            user_detail.user=user
            user_detail.save()
            messages.success(request,'کاربر ایجاد شد ')
            return redirect('/adminlte/users')
        except ValidationError as e:
            form.add_error('password',e)
        except FieldError as e:
            form.add_error('username',e)
    context={
        'form':form,
        'form2':form2,
    }
    return render(request,'add_user.html',context)

@user_passes_test(lambda u: u.has_perm('auth.view_user'),login_url='/adminlte/login')
def user_list(request):
    users=User.objects.all()
    if request.GET.get('is_admin') :
       users=users.filter(is_staff=True)
    if  request.GET.get('is_superuser') :
       users=users.filter(is_superuser=True)
    paginator = Paginator(users,20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    admins=len(User.objects.filter(is_staff=True))
    context={
        'users':users,
        'page_obj':page_obj,
        'admin_num':admins
    }
    return render(request,'user_list.html',context)



@user_passes_test(lambda u: u.has_perm('bread.change_bread'),login_url='/adminlte/login')
def edite_bread(request,id):
    form=Bread_Form(request.POST or None ,request.FILES or None,instance=Bread.objects.get(id=id))
    if form.is_valid():
        form.save()
        messages.success(request,'نان با موفیت ویرایش شد ')
        return redirect('/adminlte/bread')
    context={
        'form':form,
    }
    return render(request,'bread_edite.html',context)


@user_passes_test(lambda u: u.has_perm('bread.add_bread'),login_url='/adminlte/login')
def add_bread(request):
    form=Bread_Form(request.POST or None ,request.FILES or None )
    if form.is_valid():
        form.save()
        messages.success(request,'نان با موفقیت اضافه شد ')
        return redirect('/adminlte/bread')
    context={
        'form':form,
    }
    return render(request,'bread_add.html',context)


@user_passes_test(lambda u: u.has_perm('order.view_bread'),login_url='/adminlte/login')
def show_bread_list(request):
    breads=Bread.objects.all()
    context={
        'breads':breads,
    }
    return render(request,"bread_list.html",context)


@user_passes_test(lambda u: u.is_staff,login_url='/adminlte/login')
def dashboard(request):
    bread_num=len(Bread.objects.all())
    cart_num=len(Cart.objects.all())
    users=User.objects.all().order_by('-date_joined')[:8]
    carts=Cart.objects.all().order_by('-payment_date')[:6]
    context={
        'users':users,
        'carts':carts,
        'bread_num':bread_num,
        'cart_num':cart_num,
    }
    return render(request,'dashbord.html',context)





@user_passes_test(lambda u: u.is_superuser,login_url='/adminlte/login')
def switch_render(request):
    setting=Setting.objects.all().first()
    context={
        'is_on':setting.is_on
    }
    return render(request,'switch_render.html',context)



######################  APIs ##################################


class Get_SEll_Data(APIView):
    def get(self,request):
        c=Cart.objects.filter(is_paid=True,payment_date__year=timezone.now().year).order_by('payment_date')
        dictvalue={}
        for i in c:
            month=i.payment_date.strftime('%B')
            if i.payment_date.strftime('%B') in dictvalue:
                dictvalue[month]+=1
            else:
                dictvalue[month]=1
        context={
            'lables':dictvalue.keys(),
            'values':dictvalue.values(),
        }
        return Response(context,status=status.HTTP_200_OK)


class turn_off_or_on(APIView):
    permission_classes = (permissions.IsAuthenticated,Setting_Permission)

    def put(self, request):
        is_on=request.data.get('is_on')
        setting=Setting.objects.all().first()
        setting.is_on=bool(int(is_on))
        setting.save()
        return Response(status=status.HTTP_200_OK)


class Send_Order(APIView):
    permission_classes = (permissions.IsAuthenticated,Read_Only,Is_View_Cart)

    def get(self,request):
        cart=Cart.objects.filter(status__in=['2',"3"]).first()
        context={
                'cart':cart,
        }
        if cart is None:
            html="""
                        <div  style='display:flex;justify-content:center'>
                    <svg viewBox="0 0 100 100" style='width:300px;height:60px;margin-top:20px'  >
                        <defs>
                        <filter id="shadow">
                            <feDropShadow dx="0" dy="0" stdDeviation="1.5" 
                            flood-color="#fc6767"/>
                        </filter>
                        </defs>
                        <circle id="spinner" style="fill:transparent;stroke:#dd2476;stroke-width: 7px;stroke-linecap: round;filter:url(#shadow);" cx="50" cy="50" r="45"/>
                    </svg>
                    <br>
                    </div>
                    <h4 style='text-align:center;' class='mb-3' id='elemId'>سفارشی پیدا نشد !  درحال بارگیری</h4>
                    <br>
                """
            return Response({'html':html},status=status.HTTP_404_NOT_FOUND)
        rendered = render_to_string('change_status.html', context)
        return Response({'html':rendered},status=status.HTTP_200_OK)






class Change_Status(APIView):
    permission_classes = (permissions.IsAuthenticated,Change_Cart_Permisson)
    def post(self,request):
        cart_id=request.data.get('order_id')
        status_cart=request.data.get('status')
        cart=Cart.objects.filter(id=cart_id).first()
        cart.status=status_cart
        cart.save()
        if cart.status=='3':
            print('sms ersanl shode')
            return Response(status=status.HTTP_200_OK)
        elif cart.status=='4':
            phone=cart.user.username
            if cart.delivery_mode == '1':
                message="""
                نانوی شاپ
                نان شما تولید شد 
                در اسرع وقت به مغازه مراجعه کنید
                """
            else:
                message="""
                نانوی شاپ
                نان شما تولید شد 
                در اسرع وقت  توسط پیک برای شما ارسال میشود
                """
            send_message(phone,message)
            cart=Cart.objects.filter(status__in=['2',"3"]).first()
            if cart is None:
                html="""
                        <div  style='display:flex;justify-content:center'>
                    <svg viewBox="0 0 100 100" style='width:300px;height:60px;margin-top:20px'  >
                        <defs>
                        <filter id="shadow">
                            <feDropShadow dx="0" dy="0" stdDeviation="1.5" 
                            flood-color="#fc6767"/>
                        </filter>
                        </defs>
                        <circle id="spinner" style="fill:transparent;stroke:#dd2476;stroke-width: 7px;stroke-linecap: round;filter:url(#shadow);" cx="50" cy="50" r="45"/>
                    </svg>
                    <br>
                    </div>
                    <h4 style='text-align:center;' class='mb-3' id='elemId'>سفارشی پیدا نشد !  درحال بارگیری</h4>
                    <br>
                """
                return Response({'html':html},status=status.HTTP_404_NOT_FOUND)
            context={
                'cart':cart,
            }
            rendered = render_to_string('change_status.html', context)
            return Response({'html':rendered},status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)





class Delete_User_Item(APIView):
    permission_classes = (permissions.IsAuthenticated,User_Delete_Permission)

    def delete(self,request):
        items=request.data.getlist('items[]')
        User.objects.filter(id__in=[int(i) for i in items]).delete()
        return Response(status=status.HTTP_200_OK)



class Delete_Bread_Item(APIView):
    permission_classes = (permissions.IsAuthenticated,Bread_permission)

    def delete(self,request):
        items=request.data.getlist('items[]')
        breads=Bread.objects.filter(id__in=[int(i) for i in items]).delete()
        return Response(status=status.HTTP_200_OK)
