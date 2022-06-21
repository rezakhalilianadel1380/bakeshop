from django.db import models
from django.contrib.auth.models import User
from bread.models import Bread
# Create your models here.

class Cart(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_date=models.DateTimeField()
    delivery_mode=models.CharField(max_length=1,choices=(('1','حضوری'),('2','پیک')))
    is_paid=models.BooleanField(default=False)
    is_delivered=models.BooleanField(default=False)
    


class Cart_Item(models.Model):
    cart_id = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Bread,on_delete=models.CASCADE)
    quantity=models.IntegerField()
