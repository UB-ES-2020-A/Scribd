from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from rest_framework import generics, viewsets

from Scribd.forms import EbookForm
from Scribd.models import Ebook, User, Account
from Scribd.serializers import UserSerializer, EbookSerializer, AccountSerializer


class libro(object):

    def __init__(self, titulo, autor, descripcion):
        self.titulo = titulo
        self.autor = autor
        self.descripcion = descripcion


def base(request):
    return render(request, 'scribd/base.html')


def lista_libros(request):
    l1 = libro("El señor de los anillos la comunidad del anillo", "John R.R. Tolkien", "Thriller")
    l2 = libro("Harry potter y el prisionero de Azkaban", "Joanne Rowling", "Thriller")
    l3 = libro("Don quijote de la mancha", "Miguel de Cervantes Saavedra", "Thriller")

    libros = [l1, l2, l3, l1, l2, l3, l1, l2, l3]

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


class ebookListView(ListView):
    model = Ebook
    template_name = '../templates/jinja2/../templates/scribd/ebooks_list.html'


class ebookDetailView(DetailView):
    model = Ebook
    template_name = '../templates/jinja2/../templates/scribd/ebook_detail.html'


class EbookViewSet(viewsets.ModelViewSet):
    queryset = Ebook.objects.all().order_by('id')
    serializer_class = EbookSerializer

    # permission_classes = permissions.IsAuthenticatedOrReadOnly

    def get_queryset(self):
        return Ebook.objects.all().order_by('id')


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def base(request):
    return render(request, '../templates/jinja2/../templates/scribd/base.html')


def add_books_form(request):
    return render(request, '../templates/forms/add_book.html')


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('date_registration')
    serializer_class = AccountSerializer

    # permission_classes = permissions.IsAuthenticatedOrReadOnly

    def get_queryset(self):
        return Account.objects.all().order_by('date_registration')


def login_create_view(request):
    login_form = AuthenticationForm()
    if request.method == "POST":

        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            return redirect('/mainpage')

    # Si llegamos al final renderizamos el formulario
    return render(request, 'registration/login.html', {'form': login_form})


def signup_create_view(request):
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST, request.FILES)
        if signup_form.is_valid():
            signup_form.save()
            username = signup_form.cleaned_data.get('username')
            raw_password = signup_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('mainpage')
    else:
        signup_form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': signup_form})
