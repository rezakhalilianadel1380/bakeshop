from multiprocessing import context
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from bread.models import Bread
from order.models import Cart
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from accountt.models import Setting, User_detail
from rest_framework import status
from django.contrib import messages
from .forms import Bread_Form, User_Detail_Form,User_Form,login_form
from django.contrib.auth.password_validation import validate_password
import re
from django.core.exceptions import ValidationError,FieldError
import datetime
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth import mixins
from django.contrib.auth import logout,authenticate,login
# Create your views here.



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
    carts=Cart.objects.all()
    context={
        'carts':carts
    }
    return render(request,"orders.html",context)



class Send_Order(APIView):
    @method_decorator(user_passes_test(lambda u: u.is_superuser,login_url='/adminlte/login'))
    def get(self, request):
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
    paginator = Paginator(users,20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    admins=len(User.objects.filter(is_staff=True))
    context={
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





class Delete_User_Item(mixins.UserPassesTestMixin,APIView):
    def test_func(self):
        return self.request.user.has_perm('auth.delete_user')

    def post(self,request):
        items=request.data.getlist('items[]')
        User.objects.filter(id__in=[int(i) for i in items]).delete()
        return Response(status=status.HTTP_200_OK)



class Delete_Bread_Item(mixins.UserPassesTestMixin,APIView):
    def test_func(self):
        return self.request.user.has_perm('bread.delete_bread')
        
    def post(self,request):
        items=request.data.getlist('items[]')
        breads=Bread.objects.filter(id__in=[int(i) for i in items]).delete()
        return Response(status=status.HTTP_200_OK)



@user_passes_test(lambda u: u.has_perm('view_bread'),login_url='/adminlte/login')
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
    carts=Cart.objects.all().order_by('-payment_date')
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



class turn_off_or_on(APIView):
    @method_decorator(user_passes_test(lambda u: u.is_superuser,login_url='/adminlte/login'))
    def post(self, request):
        is_on=request.data.get('is_on')
        setting=Setting.objects.all().first()
        setting.is_on=bool(int(is_on))
        setting.save()
        return Response(status=status.HTTP_200_OK)