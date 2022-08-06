from django.shortcuts import redirect, render
from .models import Cart
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import Cart_Item
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from accountt.models import Address
from decorators.decorator import check_of_or_on
# Create your views here.

@check_of_or_on
@login_required
def cart_item_delete(request,id):
    cart=Cart.objects.filter(user=request.user,is_paid=False).first()
    cart_item=cart.cart_item.all()
    cart_item.filter(id=id).delete()
    messages.success(request,'با موفقیت حذف شد')
    return  redirect('/cart')

@check_of_or_on
def checkout(request):
    cart=Cart.objects.filter(user=request.user,is_paid=False).first()
    address=request.user.address_set.all().first()
    if address is None:
        messages.error(request,'ادرس ثبت نشده')
        return redirect('/')
    cart.address=address
    cart.save()
    if cart is None:
        return redirect('/cart')
    if not cart.is_empty():
        return redirect('/cart')
    context={
        'cart':cart
    }   
    return render(request,'checkout.html',context)

class quantity(APIView):
    @check_of_or_on
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        cart_item_id=request.data.get('cart_item_id')
        quantity=request.data.get('quantity')
        quantity_s=int(quantity)
        if quantity_s>15 or quantity_s<1:
            return Response({'er':'تعداد نان بیش از مقدار مجاز است '},status=status.HTTP_403_FORBIDDEN)
        cart_item=Cart_Item.objects.get(id=cart_item_id)
        cart_item.quantity=quantity
        cart_item.save()
        cart=Cart.objects.get(id=cart_item.cart.id)
        sum=cart.cart_total_price()
        return Response({'total_price':intcomma(sum,False)},status=status.HTTP_200_OK)

class Delivery_mode_assign(APIView):
    @check_of_or_on
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        delivery_mode=request.data.get('delivery_mode')
        cart=Cart.objects.filter(user=request.user,is_paid=False).first()
        cart.delivery_mode=delivery_mode
        cart.save()
        return Response({'delivery_mode':cart.delivery_mode},status=status.HTTP_200_OK)

class Set_Address(APIView):
    @check_of_or_on
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        address=request.data.get('address')
        cart=Cart.objects.filter(user=request.user,is_paid=False).first()
        cart.address=Address.objects.get(id=address)
        cart.save()
        return Response(status=status.HTTP_200_OK)



@check_of_or_on
@login_required
def cart(request):
    cart=Cart.objects.filter(user=request.user,is_paid=False).first()
    context={
        'cart':cart
    }
    return render(request,'cart.html',context)