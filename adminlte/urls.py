from django.urls import path
from .views import dashboard,user_list,add_bread,edite_bread,turn_off_or_on,Delete_Bread_Item,show_bread_list

urlpatterns = [
    path('',dashboard,name='dashboard'),
    path('bread',show_bread_list,name='show_bread_list'),
    path('bread/add',add_bread,name='add_bread'),
    path('bread/edite/<id>',edite_bread,name='edite_bread'),
    path('api/v1/switch',turn_off_or_on.as_view(),name='turn_off_or_on'),
    path('api/v1/delete_item',Delete_Bread_Item.as_view(),name='Delete_Bread_Item'),
    path('users',user_list,name='user_list'),
]