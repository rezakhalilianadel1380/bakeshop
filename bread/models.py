from turtle import title
from django.db import models

# Create your models here.



class Bread(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='bread/images/')
    price=models.DecimalField(max_digits=10,decimal_places=0)

    def __str__(self) -> str:
        return self.title
