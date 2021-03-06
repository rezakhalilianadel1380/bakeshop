from django.urls import path
from .views import (
dashboard,user_list,
produce_bread,
edite_user,add_user,
Delete_User_Item,
Send_Order,Change_Status,
add_bread,edite_bread,
turn_off_or_on,
Delete_Bread_Item,
show_bread_list,
show_orders,
admin_logout,
admin_login
)

urlpatterns = [
    path('',dashboard,name='dashboard'),
    path('bread',show_bread_list,name='show_bread_list'),
    path('bread/add',add_bread,name='add_bread'),
    path('bread/edite/<id>',edite_bread,name='edite_bread'),
    path('users',user_list,name='user_list'),
    path('user/add',add_user,name='add_user'),
    path('user/edite/<id>',edite_user,name='edite_user'),
    path('produce/bread',produce_bread,name='produce_bread'),
    path('show_orders',show_orders,name='show_orders'),
    path('logout',admin_logout,name='admin_logout'),
    path('login',admin_login,name='admin_login'),
    # APIs
    path('api/v1/produce/bread',Change_Status.as_view(),name='Change_Status'),
    path('api/v1/produce/bread/read',Send_Order.as_view(),name='read_order'),
    path('api/v1/switch',turn_off_or_on.as_view(),name='turn_off_or_on'),
    path('api/v1/delete_item',Delete_Bread_Item.as_view(),name='Delete_Bread_Item'),
    path('api/v1/delete_user_item',Delete_User_Item.as_view(),name='Delete_User_Item'),
]