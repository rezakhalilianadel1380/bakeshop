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
log_out,
profile_dashbord,
edite_account,
show_orders_profile,
show_addresses_in_profile,
add_address,
edite_address,
delete_address,
change_password,
change_phone,
Change_Phone_Confirm_code,
Change_New_Phone_Confirm_code,
forget_password,
Check_Phone_forget_password,
Check_The_Code_Forget_Password,
Assign_Password
 )
 
urlpatterns = [
    path('signin',login2,name='login_page'),
    path('log_out',log_out,name='log_out'),
    path('signup',sign_upv2,name='sign_up'),
    path('signin/forget_password',forget_password,name='forget_password'),
    path('about_us',about_us,name='about-us'),
    path('contact_us',contact_us,name='contact-us'),
    path('profile/DashBoard',profile_dashbord,name='profile_dashbord'),
    path('profile/EditeProfile',edite_account,name='edite_account'),
    path('profile/orders',show_orders_profile,name='show_orders_profile'),
    path('profile/Address',show_addresses_in_profile,name='show_addresses_in_profile'),
    path('profile/Address/Add',add_address,name='add_address'),
    path('profile/Address/Edite/<id>',edite_address,name='edite_address'),
    path('profile/Address/Delete/<id>',delete_address,name='delete_address'),
    path('profile/changepassword',change_password,name='change_password'),
    path('profile/change_phone',change_phone,name='change_phone'),
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
    #change_phone APIs
    path('api/v1/change_phone/send_code/old',Change_Phone_Confirm_code.as_view(),name='Change_Phone_Confirm_code'),
    path('api/v1/change_phone/send_code/new',Change_New_Phone_Confirm_code.as_view(),name='Change_New_Phone_Confirm_code'),
    #forget_passwrod APIs
    path('api/v1/forget_password_send',Check_Phone_forget_password.as_view(),name='forget_password_send_sms'),
    path('api/v1/forget_password_send_code',Check_The_Code_Forget_Password.as_view(),name='Check_The_Code_Forget_Password'),
    path('api/v1/forget_password_assign_Password',Assign_Password.as_view(),name='Assign_Password'),

]


