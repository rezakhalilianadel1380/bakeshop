from django.urls import path
from order.views import cart, cart_item_delete, checkout,quantity


urlpatterns = [
    path('cart',cart,name='cart'),
    path('quantity',quantity.as_view(),name='quantity'),
    path('checkout',checkout,name='checkout'),
    path('delete_item/<id>',cart_item_delete,name='delete_item'),
]