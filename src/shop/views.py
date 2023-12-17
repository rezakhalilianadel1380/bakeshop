from django.shortcuts import redirect, render
from bread.models import Bread
from order.forms import Cart_Form
from django.contrib import messages
from order.models import Cart,Cart_Item
from decorators.decorator import check_of_or_on
from bread.forms import Bread_Form


def partial_breadform(request,bread):
    form=Bread_Form()
    bread_attr=bread.bread_attr.all()
    form.fields['bread_attr'].choices=[ (i.id,f"{i.title} - {i.price}+") for i in bread_attr]
    form.fields['bread_attr'].choices.insert(0, (0,"ساده"))
    context={
        'form':form,
    }
    return render(request,'breadattr.html',context)



@check_of_or_on
def homepage(request):
    breads=Bread.objects.all()
    form=Cart_Form(request.POST or None)
    form2=Bread_Form(request.POST or None)
    if form.is_valid() and  form2.is_valid():
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
            cart=Cart.objects.create(user_id=request.user.id,status='1')
            cart_item=Cart_Item.objects.create(cart=cart,bread_id=bread_id,quantity=quantity)
            messages.success(request,'با موفقیت به سبد خرید شما اضافه شد ')
            return redirect('/')
    if form.errors:
       for i in form:
            for j in i.errors:
                messages.error(request,j)
    context={
        'breads':breads,
        'form':form,
        'form2':form2,
        }
    return render(request,'homepage.html',context)


