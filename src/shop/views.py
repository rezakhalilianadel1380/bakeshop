from django.shortcuts import redirect, render
from bread.models import Bread,Bread_Attr
from order.forms import Cart_Form
from django.contrib import messages
from order.models import Cart,Cart_Item
from decorators.decorator import check_of_or_on
from bread.forms import Bread_Form
from django.contrib.auth.hashers import make_password, check_password


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
    if request.method == 'POST' and request.POST.get('bread_attr') is not None:
        BreadID=request.POST.get('bread_id')
        bread_attr=Bread.objects.get(id=BreadID).bread_attr.all()
        form2.fields['bread_attr'].choices=[ (i.id,f"{i.title} - {i.price}+") for i in bread_attr]
        form2.fields['bread_attr'].choices.insert(0, (0,"ساده"))
    if form.is_valid() and form2.is_valid():
        if not request.user.is_authenticated:
            return redirect('/signin')
        quantity=form.cleaned_data.get('quantity')
        bread_id=form.cleaned_data.get('bread_id')
        bread_attr=form2.cleaned_data.get('bread_attr')
        print(bread_attr)
        cart=Cart.objects.filter(user=request.user,is_paid=False)
        if cart:
            cart_item=Cart_Item.objects.filter(cart=cart.first(),bread_id=bread_id)
            if cart_item.exists():
                messages.error(request,'این محصول در سبد خرید شما موجود است')
                return redirect('/')
            else:
                cart_item=Cart_Item.objects.create(cart=cart.first(),bread_id=bread_id,quantity=quantity)
                cart_item.price=cart_item.bread.base_price
                if bread_attr:
                    if bread_attr !='0':
                        bread_attr_obj=Bread_Attr.objects.filter(id=bread_attr).first()
                        cart_item.bread_attr=bread_attr_obj
                        cart_item.price=cart_item.bread.base_price+bread_attr_obj.price
                cart_item.save()
                messages.success(request,'با موفقیت به سبد خرید شما اضافه شد ')
                return redirect('/')
        else:
            cart=Cart.objects.create(user_id=request.user.id,status='1')
            cart_item=Cart_Item.objects.create(cart=cart,bread_id=bread_id,quantity=quantity)
            cart_item.price=cart_item.bread.base_price
            if bread_attr !='0':
                bread_attr_obj=Bread_Attr.objects.filter(id=int(bread_attr)).first()
                cart_item.bread_attr=bread_attr_obj
                cart_item.price=cart_item.bread.base_price+bread_attr_obj.price
            cart_item.save()
            messages.success(request,'با موفقیت به سبد خرید شما اضافه شد ')
            return redirect('/')
    if form.errors :
       for i in form:
            for j in i.errors:
                messages.error(request,j)
    context={
        'breads':breads,
        'form':form,
        'form2':form2,
        }
    return render(request,'homepage.html',context)


