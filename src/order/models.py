from dis import dis
from pickle import TRUE
from pyexpat import model
from telnetlib import STATUS
from tkinter import N
from turtle import title
from typing import final
from django.db import models
from django.contrib.auth.models import User
from bread.models import Bread
from accountt.models import Address
from bread.models import Bread_Attr
# Create your models here.


class Discount(models.Model):
    discount_code=models.CharField(max_length=50,unique=True)
    dicount_percent=models.IntegerField(default=1)
    max_price_dicount=models.IntegerField(default=0)
    price_after_max_price=models.IntegerField(default=0)
    active=models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.discount_code

status_choices=(
    ('1','در انتظار پرداخت'),
    ('2','در انتظار تولید'),
    ('3','در حال تولید'),
    ('4','تولید شده '),
    ('5','تحویل داده شده'),

)

class Cart(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    payment_date=models.DateTimeField(null=True,blank=True)
    delivery_mode=models.CharField(max_length=1,choices=(('1','حضوری'),('2','پیک')),default='1')
    is_paid=models.BooleanField(default=False)
    status=models.CharField(max_length=1,choices=status_choices,blank=True,default='1')
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,blank=True)
    discount=models.ForeignKey(Discount,on_delete=models.SET_NULL,null=True,blank=True)
    bag=models.CharField(max_length=1,choices=(('1','کاغذی'),('2','پلاستیکی')),default='1')

    class Meta:
        permissions = [
            ("can_view_cart", "میتونه سفارش ها رو مشاهده کنه"),
            ("can_access_produce_section","دسترسی به بخش تولید نان "),
        ]
    
    def __str__(self) -> str:
        return self.user.username

    def get_bread_title(self):
        cart_items=self.cart_item.all()
        titles=[]
        for cart_item in cart_items:
            titles.append(cart_item.bread.title)
        return ','.join(titles)
        

    def is_empty(self):
        cart_item=self.cart_item.all()
        if cart_item:
            return True
        return False
    
    def cart_total_price(self):
        sum=0
        cart_item=self.cart_item.all()
        for i in cart_item:
            sum+=i.price*i.quantity
        return sum

    def calculate_discount(self) -> tuple:
        """ reuturn  final base_price and discount price return tuple """
        discount=self.discount
        total_price=int(self.cart_total_price())
        final_price=0 
        discount_price=0
        if total_price<= discount.max_price_dicount:
            discount_price=int(total_price*(discount.dicount_percent/100))
            final_price=total_price - discount_price
        else:
            discount_price=discount.price_after_max_price
            final_price=total_price-int(discount.price_after_max_price)

        return int(final_price),int(discount_price)


    def get_lable_color(self):
        if self.status =='1':
            return 'label-warning'
        elif self.status =='2':
            return 'label-warning'
        elif self.status =='3':
            return 'label-info'
        elif self.status =='4':
            return 'label-danger'
        elif self.status =='5':
            return 'label-success'



class Cart_Item(models.Model):
    cart= models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_item')
    bread= models.ForeignKey(Bread,on_delete=models.CASCADE)
    bread_attr=models.ForeignKey(Bread_Attr,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=0,default=0)

    def __str__(self) -> str:
        return self.cart.user.username
    

    def calculate_price(self):
        return self.price*self.quantity



