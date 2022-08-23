from email.policy import default
from pyexpat import model
from sre_parse import State
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
# Create your models here.

class Setting(models.Model):
    is_on=models.BooleanField(default=True)
    limit_buy=models.IntegerField(default=15)
    limit_day=models.IntegerField(default=7000)

    def __str__(self):
        return f'{self.is_on}'


state_choices=(
    ('khorasan_razavi','خراسان رضوی'),
)

city_choices=(
    ('mashhad','مشهد'),
)



class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    state=models.CharField(default='khorasan_razavi',choices=state_choices,max_length=50)
    city=models.CharField(default='mashhad',choices=city_choices,max_length=50)
    address=models.TextField()
    pelak=models.CharField(max_length=20,null=True)
    vahed=models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.address

    def get_address(self):
        return f' {self.get_state_display()} , {self.get_city_display()} ,{self.address} , پلاک {self.pelak}   ,  واحد {self.vahed} '



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






