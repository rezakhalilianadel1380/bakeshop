from multiprocessing import context
from django.shortcuts import render
from bread.models import Bread
from order.models import Cart
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from accountt.models import Setting
from rest_framework import status
# Create your views here.





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