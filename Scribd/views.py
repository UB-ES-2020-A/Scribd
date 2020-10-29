from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView

from Scribd.models import Ebook, Account
from Scribd.forms import EbookForm
from Scribd.serializers import EbookSerializer, AccountSerializer
from rest_framework import generics, viewsets, permissions
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


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


class ebookListView(ListView):
    model = Ebook
    template_name = '../templates/scribd/ebooks_list.html'


class ebookDetailView(DetailView):
    model = Ebook
    template_name = '../templates/scribd/ebook_detail.html'


class EbookViewSet(viewsets.ModelViewSet):
    queryset = Ebook.objects.all().order_by('id')
    serializer_class = EbookSerializer
    # permission_classes = permissions.IsAuthenticatedOrReadOnly

    def get_queryset(self):
        return Ebook.objects.all().order_by('id')

# ------------------------------------------User management------------------------------------------------


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
    return render(request, '../templates/registration/login.html', {'form': login_form})


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
    return render(request, '../templates/registration/signup.html', {'form': signup_form})