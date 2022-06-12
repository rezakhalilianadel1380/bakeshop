from django.shortcuts import render
from bread.models import Bread

def homepage(request):
    breads=Bread.objects.all()
    context={
        'breads':breads
        }
    return render(request,'homepage.html',context)