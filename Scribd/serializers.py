from rest_framework import serializers
from .models import Account, SubscribedAccounts

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'name', 'email', 'date_registration', 'subscription', 'type')


