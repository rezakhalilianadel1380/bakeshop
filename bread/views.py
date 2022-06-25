from django.shortcuts import render
from rest_framework.views import APIView
from .models import Bread
from rest_framework.response import Response
from .models import Bread
from rest_framework import status

# Create your views here.


class Add_To_favorite(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        bread=request.data.get('bread_id')
        bread=Bread.objects.get(id=bread)
        user_id=request.user.id
        bread.users.add(user_id)
        return Response(status=status.HTTP_200_OK)


class Delete_from_favorite(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        bread=request.data.get('bread_id')
        bread=Bread.objects.get(id=bread)
        user_id=request.user.id
        bread.users.remove(user_id)
        return Response(status=status.HTTP_200_OK)

