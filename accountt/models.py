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

    def get_image(self):
        if self.image:
            return self.image.url
        return static("adminlte/dist/img/avatar5.png")



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






