from django.shortcuts import render

# Create your views here.

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
