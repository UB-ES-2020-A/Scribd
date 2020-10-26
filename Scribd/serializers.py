from rest_framework import serializers

from Scribd.models import Ebook
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'name', 'email', 'date_registration', 'subscription', 'type')


class ebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ebook
        fields = ('id', 'title', 'autor', 'size', 'media_type', 'count_downloads')
