from django.shortcuts import render
from Scribd.models import Ebook
from Scribd.serializers import ebookSerializer
from rest_framework import generics


# Create your views here.

# GET/POST
class libro(object):

    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor

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
