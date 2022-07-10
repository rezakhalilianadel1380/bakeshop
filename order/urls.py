from django.urls import path
from order.views import Delivery_mode_assign, Set_Address, cart, cart_item_delete, checkout,quantity


urlpatterns = [
    path('cart',cart,name='cart'),
    path('quantity',quantity.as_view(),name='quantity'),
    path('delivery_mode',Delivery_mode_assign.as_view(),name='delivery_mode'),
    path('Set_Address',Set_Address.as_view(),name='Set_Address'),
    path('checkout',checkout,name='checkout'),
    path('delete_item/<id>',cart_item_delete,name='delete_item'),
]