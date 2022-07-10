from multiprocessing import context
from django.shortcuts import render
from bread.models import Bread
from order.models import Cart
from django.contrib.auth.models import User

# Create your views here.



def dashboard(request):
    bread_num=len(Bread.objects.all())
    cart_num=len(Cart.objects.all())
    user_num=len(User.objects.all())
    context={
        'bread_num':bread_num,
        'cart_num':cart_num,
        'user_num':user_num,
    }
    return render(request,'dashbord.html',context)