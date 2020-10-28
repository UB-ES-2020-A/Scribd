from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView

from Scribd.models import Ebook
from Scribd.forms import EbookForm, UserLoginForm
from Scribd.serializers import ebookSerializer
from rest_framework import generics
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
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
    
def ebook_create_view(request):
    if request.method == 'POST':
        form = EbookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ebook_custom_list')
    else:
        form = EbookForm()
    return render(request, '../templates/forms/add_book.html', {'form': form})

def login_create_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('mainpage')
    else:
        form = EbookForm()
    return render(request, '../templates/registration/login.html', {'form': form})

class ebookListView(ListView):
    model = Ebook
    template_name = '../templates/scribd/ebooks_list.html'


class ebookDetailView(DetailView):
    model = Ebook
    template_name = '../templates/scribd/ebook_detail.html'


class ebookList(generics.ListCreateAPIView):
    queryset = Ebook.objects.all()
    serializer_class = ebookSerializer


class ebookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ebook.objects.all()
    serializer_class = ebookSerializer


def base(request):
    return render(request, '../templates/scribd/base.html')



def add_books_form(request):
    return render(request, '../templates/forms/add_book.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})