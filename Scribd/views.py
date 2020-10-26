from django.shortcuts import render
from Scribd.models import Account
from Scribd.serializers import AccountSerializer
from rest_framework import generics

# Create your views here.

#GET/POST

class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all().order_by('username')
    serializer_class = AccountSerializer

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer