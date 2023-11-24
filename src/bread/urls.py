
from django.urls import path,include
from .views import Add_To_favorite,Delete_from_favorite

urlpatterns = [
    path('add-to-favorite',Add_To_favorite.as_view()),
    path('Delete-from-favorite',Delete_from_favorite.as_view()),
]


