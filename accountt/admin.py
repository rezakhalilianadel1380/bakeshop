from re import A
from django.contrib import admin
from .models import Address, Setting, User_detail, Code,Sign_up,STate,City
from django.contrib.auth.models import Permission
# Register your models here.
admin.site.register(User_detail)
admin.site.register(Code)
admin.site.register(Sign_up)
admin.site.register(Address)
admin.site.register(Setting)
admin.site.register(STate)
admin.site.register(City)