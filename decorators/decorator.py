from accountt.models import Setting
from django.shortcuts import redirect, render

def check_of_or_on(fnc):
    def wrapper(request,*args,**kwargs):
        setting=Setting.objects.all().first()
        if setting.is_on:
            return fnc(request,*args,**kwargs)
        else:
            return render(request,'close.html')
    return wrapper
