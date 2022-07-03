from django.shortcuts import redirect, render
from bread.models import Bread
from order.forms import Cart_Form
from django.contrib import messages
from order.models import Cart,Cart_Item




def homepage(request):
    breads=Bread.objects.all()
    form=Cart_Form(request.POST or None)
    if form.is_valid():
        if not request.user.is_authenticated:
            return redirect('/login')
        quantity=form.cleaned_data.get('quantity')
        bread_id=form.cleaned_data.get('bread_id')
        cart=Cart.objects.filter(user=request.user,is_paid=False)
        if cart:
            cart_item=Cart_Item.objects.filter(cart=cart.first(),bread_id=bread_id)
            if cart_item:
                messages.error(request,'این محصول در سبد خرید شما موجود است')
                return redirect('/')
            else:
                cart_item=Cart_Item.objects.create(cart=cart.first(),bread_id=bread_id,quantity=quantity)
                messages.success(request,'با موفقیت به سبد خرید شما اضافه شد ')
                return redirect('/')
        else:
            cart=Cart.objects.create(user_id=request.user.id)
            cart_item=Cart_Item.objects.create(cart=cart,bread_id=bread_id,quantity=quantity)
            messages.success(request,'با موفقیت به سبد خرید شما اضافه شد ')
            return redirect('/')
    if form.errors:
       for i in form:
            for j in i.errors:
                messages.error(request,j)
    context={
        'breads':breads,
        'form':form
        }
    return render(request,'homepage.html',context)