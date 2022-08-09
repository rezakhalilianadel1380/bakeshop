from re import A
from django.contrib import admin
from .models import Address, Setting, User_detail
from .models import Code,Sign_up
from django.contrib.auth.models import Permission
# Register your models here.
admin.site.register(User_detail)
admin.site.register(Code)
admin.site.register(Sign_up)
admin.site.register(Address)
admin.site.register(Setting)