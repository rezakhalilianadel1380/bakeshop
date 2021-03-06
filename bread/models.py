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
    price=models.DecimalField(max_digits=10,decimal_places=0)
    users=models.ManyToManyField(User,blank=True)

    def __str__(self) -> str:
        return self.title

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

