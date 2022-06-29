from django.urls import path
from order.views import cart,quantity
urlpatterns = [
    path('cart',cart,name='cart'),
    path('quantity',quantity.as_view(),name='quantity'),
]