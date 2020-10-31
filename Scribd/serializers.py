from rest_framework import serializers

from Scribd.models import Ebook
from .user_model import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ebook
        fields = '__all__'
