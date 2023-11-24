from email.policy import default
from enum import unique
from pyexpat import model
from sre_parse import State
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

# Create your models here.


class Authenticated_Code(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    authentication_code=models.CharField(max_length=20,unique=True)
    create_time=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.authentication_code






class Setting(models.Model):
    is_on=models.BooleanField(default=True)
    limit_buy=models.IntegerField(default=15)
    limit_day=models.IntegerField(default=7000)

    def __str__(self):
        return f'{self.is_on}'


class STate(models.Model):
    state_code=models.CharField(max_length=50)
    state_title_fa=models.CharField(max_length=50)
    state_title_en=models.CharField(max_length=50)

    
    def __str__(self) -> str:
        return self.state_title_fa


class City(models.Model):
    city_code=models.CharField(max_length=50)
    state=models.ForeignKey(STate,on_delete=models.CASCADE,null=True)
    city_title_fa=models.CharField(max_length=50)
    city_title_en=models.CharField(max_length=50)
    is_activated=models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.city_title_fa

class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    state=models.ForeignKey(STate,on_delete=models.CASCADE,null=True)
    city=models.ForeignKey(City,on_delete=models.CASCADE,null=True)
    address=models.TextField()
    pelak=models.IntegerField(null=True)
    vahed=models.IntegerField(null=True)
    lat=models.FloatField(null=True)
    lon=models.FloatField(null=True)


    def __str__(self):
        return self.address

    def get_address(self):
        return f' {self.state.state_title_fa} , {self.city.city_title_fa} ,{self.address} , پلاک {self.pelak}   ,  واحد {self.vahed} '



class User_detail(models.Model):
    image=models.ImageField(upload_to='avatar/',null=True,blank=True) 
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

    def get_image(self):
        if self.image:
            return self.image.url
        return static("adminlte/dist/img/avatar5.png")



class Code(models.Model):
    code=models.CharField(max_length=6,blank=True,null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    expired_time=models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.code

   


class Sign_up(models.Model):
    phone_number=models.CharField(max_length=11,unique=True)
    code=models.CharField(max_length=6,null=True,blank=True)
    expired_time=models.DateTimeField(null=True)

    def __str__(self):
        return self.phone_number






