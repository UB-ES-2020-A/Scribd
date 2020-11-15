from rest_framework import serializers
from Scribd.models import Ebook, UploadedResources, UserTickets
from .user_model import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ebook
        fields = '__all__'

        
class UploadResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedResources
        fields = '__all__'

        
class ticketSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTickets
        fields = '__all__'


