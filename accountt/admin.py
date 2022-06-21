from re import A
from django.contrib import admin
from .models import Address, User_detail
from .models import Code
# Register your models here.
admin.site.register(User_detail)
admin.site.register(Code)
admin.site.register(Address)