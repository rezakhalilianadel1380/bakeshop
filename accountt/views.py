from django.shortcuts import render

# Create your views here.


def login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        

    return render(request,'login.html',{})