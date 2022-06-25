import re
from django.shortcuts import redirect, render
from bread.models import Bread
from order.forms import Cart_Form
from django.contrib import messages
from order.models import Cart,Cart_Item


def homepage(request):
    breads=Bread.objects.all()
    form=Cart_Form(request.POST or None,initial={'radio_type':"1"})
    if form.is_valid():
        if not request.user.is_authenticated:
            return redirect('/login')
        quantity=form.cleaned_data.get('quantity')
        product_id=form.cleaned_data.get('product_id')
        radio_type=form.cleaned_data.get('radio_type')
        cart=Cart.objects.filter(user=request.user,is_paid=False)
        if cart:
            cart_item=Cart_Item.objects.filter(cart_id=cart.id,product_id=product_id)
            if cart_item:
                messages.error(request,'این محصول در سبد خرید شما موجود است')
                return redirect('/')
            else:
                cart_item=Cart_Item.objects.create(cart_id=cart.first().id,product_id=product_id,quantity=quantity)
        else:
            cart=Cart.objects.create(user_id=request.user.id)
            cart_item=Cart_Item.objects.create(cart_id=cart,product_id=product_id,quantity=quantity)
    
    context={
        'breads':breads,
        'form':form
        }
    return render(request,'homepage.html',context)