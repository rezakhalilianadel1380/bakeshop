from django.urls import path
from accountt.views import about_us,login2,Resend,Check_The_Code,Send_The_Code,Check_Password,Check_Phone, contact_us, log_out, register, sign_up, sign_up_code
urlpatterns = [
    path('signin',login2,name='login_page'),
    path('log_out',log_out,name='log_out'),
    path('signup',sign_up,name='sign_up'),
    path('signup/code',sign_up_code,name='sign_up_code'),
    path('signup/register',register,name='register'),
    path('about_us',about_us,name='about-us'),
    path('contact_us',contact_us,name='contact-us'),
    path('api/v1/step1',Check_Phone.as_view(),name='Check_Phone'),
    path('api/v1/step2',Check_Password.as_view(),name='Check_Password'),
    path('api/v1/Send_The_Code',Send_The_Code.as_view(),name='Send_The_Code'),
    path('api/v1/step3',Check_The_Code.as_view(),name='Check_The_Code'),
    path('api/v1/Resend',Resend.as_view(),name='Resend'),
]


