from telnetlib import STATUS
from django.db import models
from django.contrib.auth.models import User
from bread.models import Bread
from accountt.models import Address
# Create your models here.

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
    
    def __str__(self) -> str:
        return self.user.username

    def is_empty(self):
        cart_item=self.cart_item.all()
        if cart_item:
            return True
        return False
    
    def cart_total_price(self):
        sum=0
        cart_item=self.cart_item.all()
        for i in cart_item:
            sum+=i.bread.price*i.quantity
        return sum

    def get_lable_color(self):
        if self.status =='1':
            return 'label-warning'
        if self.status =='2':
            return 'label-warning'
        if self.status =='3':
            return 'label-info'
        if self.status =='4':
            return 'label-danger'
        if self.status =='5':
            return 'label-success'



class Cart_Item(models.Model):
    cart= models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_item')
    bread= models.ForeignKey(Bread,on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self) -> str:
        return self.cart.user.username
