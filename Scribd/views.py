from django.shortcuts import render
from rest_framework import generics

from Scribd.models import Account
from Scribd.models import Ebook
from Scribd.serializers import AccountSerializer
from Scribd.serializers import ebookSerializer


# Create your views here.

# GET/POST
class libro(object):

    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor


def base(request):
    return render(request, 'scribd/base.html')


def lista_libros(request):
    l1 = libro("el señor de los anillos la comunidad del anillo", "John R.R. Tolkien")
    l2 = libro("harry potter y las reliquias de la muerte", "Joanne Rowling")
    l3 = libro("don quijote de la mancha", "Miguel de Cervantes Saavedra")

    libros = [l1, l2, l3]

    ctx = {"lista_libros": libros}

    return render(request, "scribd/mainpage.html", ctx)


class ebookList(generics.ListCreateAPIView):
    queryset = Ebook.objects.all()
    serializer_class = ebookSerializer


# GET/PATCH (AKA PUT)/DELETE
class ebookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ebook.objects.all()
    serializer_class = ebookSerializer


# Create your views here.

# GET/POST

class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all().order_by('username')
    serializer_class = AccountSerializer


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
