from django.db import models
from django.contrib.auth.models import User
from bread.models import Bread
# Create your models here.

class Cart(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    payment_date=models.DateTimeField(null=True,blank=True)
    delivery_mode=models.CharField(max_length=1,choices=(('1','حضوری'),('2','پیک')),blank=True)
    is_paid=models.BooleanField(default=False)
    is_delivered=models.BooleanField(default=False)
    
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



class Cart_Item(models.Model):
    cart= models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_item')
    bread= models.ForeignKey(Bread,on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self) -> str:
        return self.cart.user.username
