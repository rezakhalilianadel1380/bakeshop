from turtle import title
from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.



class Bread(models.Model):
    title=models.CharField(max_length=100)
    description=RichTextUploadingField()
    image=models.ImageField(upload_to='bread/images/')
    base_price=models.DecimalField(max_digits=10,decimal_places=0)
    users=models.ManyToManyField(User,blank=True)
    is_attr=models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
    
    def get_price(self):
        if self.is_attr:
            bread_attr=self.bread_attr.all().first()
            return self.base_price + bread_attr.price
        return self.base_price


    def favorite(self):
        users=self.users.all()
        return users

    def count_sell_bread(self):
        c=apps.get_model('order','CART')
        carts=c.objects.filter(is_paid=True,cart_item__bread=self)
        sum=0
        for cart in carts:
            cart_item=cart.cart_item.filter(bread=self).first()
            sum+=cart_item.quantity
        return sum


class Bread_Attr(models.Model):
    title=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10,decimal_places=0)
    bread=models.ForeignKey(Bread,on_delete=models.CASCADE,related_name="bread_attr")

    def __str__(self) -> str:
        return self.title


