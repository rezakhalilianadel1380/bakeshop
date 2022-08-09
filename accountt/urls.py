from django.urls import path

from accountt.views import (
Register_User,
Resend_Code,
about_us,sign_upv2,
Check_Code_Sign_Up,
Check_Phone_Sign_Up,
login2,
Resend,
Check_The_Code,
Send_The_Code,
Check_Password,
Check_Phone,
contact_us, 
log_out

 )
 
urlpatterns = [
    path('signin',login2,name='login_page'),
    path('log_out',log_out,name='log_out'),
    path('signup',sign_upv2,name='sign_up'),
    path('about_us',about_us,name='about-us'),
    path('contact_us',contact_us,name='contact-us'),
    #signup APIs
    path('api/v1/signup/step1',Check_Phone_Sign_Up.as_view(),name='Check_Phone_Sign_Up'),
    path('api/v1/signup/step2',Check_Code_Sign_Up.as_view(),name='Check_Code_Sign_Up'),
    path('api/v1/signup/step3',Register_User.as_view(),name='Register_User'),
    path('api/v1/signup/resend',Resend_Code.as_view(),name='Resend_Code'),
    #login APIs
    path('api/v1/step1',Check_Phone.as_view(),name='Check_Phone'),
    path('api/v1/step2',Check_Password.as_view(),name='Check_Password'),
    path('api/v1/Send_The_Code',Send_The_Code.as_view(),name='Send_The_Code'),
    path('api/v1/step3',Check_The_Code.as_view(),name='Check_The_Code'),
    path('api/v1/Resend',Resend.as_view(),name='Resend'),
]


