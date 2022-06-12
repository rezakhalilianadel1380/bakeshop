from django.urls import path
from accountt.views import login

urlpatterns = [
    path('login',login,name='login_page'),
]


