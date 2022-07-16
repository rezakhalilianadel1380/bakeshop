from multiprocessing import context
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from bread.models import Bread
from order.models import Cart
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from accountt.models import Setting
from rest_framework import status
from django.contrib import messages
from .forms import Bread_Form
# Create your views here.


def user_list(request):
    users=User.objects.all()
    admins=len(User.objects.filter(is_staff=True))
    context={
        'users':users,
        'admin_num':admins
    }
    return render(request,'user_list.html',context)


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





class Delete_Bread_Item(APIView):
    def post(self,request):
        items=request.data.getlist('items[]')
        breads=Bread.objects.filter(id__in=[int(i) for i in items]).delete()
        return Response(status=status.HTTP_200_OK)




def show_bread_list(request):
    breads=Bread.objects.all()
    context={
        'breads':breads,
    }
    return render(request,"bread_list.html",context)

def dashboard(request):
    bread_num=len(Bread.objects.all())
    cart_num=len(Cart.objects.all())
    users=User.objects.all().order_by('-date_joined')[:10]
    carts=Cart.objects.all().order_by('payment_date')
    context={
        'users':users,
        'carts':carts,
        'bread_num':bread_num,
        'cart_num':cart_num,
    }
    return render(request,'dashbord.html',context)


def switch_render(request):
    setting=Setting.objects.all().first()
    context={
        'is_on':setting.is_on
    }
    return render(request,'switch_render.html',context)

class turn_off_or_on(APIView):
    def post(self, request):
        is_on=request.data.get('is_on')
        setting=Setting.objects.all().first()
        setting.is_on=bool(int(is_on))
        setting.save()
        return Response(status=status.HTTP_200_OK)