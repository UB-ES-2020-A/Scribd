from django.shortcuts import render
from Scribd.models import ebook
from Scribd.serializers import ebookSerializer
from rest_framework import generics


# Create your views here.

# GET/POST
class ebookList(generics.ListCreateAPIView):
    queryset = ebook.objects.all()
    serializer_class = ebookSerializer


# GET/PATCH (AKA PUT)/DELETE
class ebookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ebook.objects.all()
    serializer_class = ebookSerializer
