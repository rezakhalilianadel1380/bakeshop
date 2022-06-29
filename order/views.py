from django.shortcuts import render
from .models import Cart
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import Cart_Item
from django.contrib.humanize.templatetags.humanize import intcomma
# Create your views here.

class quantity(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        cart_item_id=request.data.get('cart_item_id')
        quantity=request.data.get('quantity')
        cart_item=Cart_Item.objects.get(id=cart_item_id)
        cart_item.quantity=quantity
        cart_item.save()
        cart=Cart.objects.get(id=cart_item.cart.id)
        sum=cart.cart_total_price()
        return Response({'total_price':intcomma(sum)},status=status.HTTP_200_OK)

@login_required(login_url='/login')
def cart(request):
    cart=Cart.objects.filter(user=request.user,is_paid=False).first()
    context={
        'cart':cart
    }
    return render(request,'cart.html',context)