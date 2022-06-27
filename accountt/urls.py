from django.urls import path
from accountt.views import about_us, contact_us, login_code, log_out, login_page, login_password, register, sign_up, sign_up_code

urlpatterns = [
    path('login',login_page,name='login_page'),
    path('login/password',login_password,name='login_password_page'),
    path('logout',log_out,name='log_out'),
    path('login/code',login_code,name='login_code'),
    path('signup',sign_up,name='sign_up'),
    path('signup/code',sign_up_code,name='sign_up_code'),
    path('signup/register',register,name='register'),
    path('about_us',about_us,name='about-us'),
    path('contact_us',contact_us,name='contact-us'),
]


