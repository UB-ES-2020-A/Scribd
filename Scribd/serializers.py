from rest_framework import serializers

from Scribd.models import Ebook, userTickets
from .user_model import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ebook
        fields = '__all__'

class ticketSerializer(serializers.ModelSerializer):
    class Meta:
        model = userTickets
        fields = '__all__'

