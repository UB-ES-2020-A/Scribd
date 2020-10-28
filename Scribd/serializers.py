from rest_framework import serializers

from Scribd.models import Ebook
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'name', 'password', 'email', 'date_registration', 'subscription', 'type')


class ebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ebook
        fields = '__all__'