from django.contrib import admin
from .models import Cart,Discount,Cart_Item
# Register your models here.

admin.site.register(Cart)
admin.site.register(Cart_Item)
admin.site.register(Discount)