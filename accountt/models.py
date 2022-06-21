from django.db import models
from django.contrib.auth.models import User
import uuid
from bread.models import Bread
# Create your models here.


class User_Favorite_Breads(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE)


    def __str__(self):
        return self.bread.name



class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.TextField()

    def __str__(self):
        return self.address

class User_detail(models.Model):
    phone_number=models.CharField(max_length=11,unique=True)
    image=models.ImageField(upload_to='avatar/',null=True,blank=True) 
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.phone_number



class Code(models.Model):
    code=models.CharField(unique=True,max_length=6)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    expired_time=models.DateTimeField()

    def __str__(self):
        return self.code



class Sign_up(models.Model):
    phone_number=models.CharField(max_length=11,unique=True)
    code=models.CharField(unique=True,max_length=6)
    expired_time=models.DateTimeField(null=True)

    def __str__(self):
        return self.phone_number






