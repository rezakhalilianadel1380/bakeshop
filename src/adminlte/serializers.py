from rest_framework import serializers
from bread.models import Bread


class Bread_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Bread
        fields="__all__"