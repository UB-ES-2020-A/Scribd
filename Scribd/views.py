from datetime import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from rest_framework import generics

from Scribd.forms import EbookForm, RegisterForm
from Scribd.models import Ebook
from Scribd.user_model import User, UserManager
from Scribd.serializers import UserSerializer
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


class ebookList(generics.ListCreateAPIView):
    queryset = Ebook.objects.all()
    serializer_class = ebookSerializer


class ebookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ebook.objects.all()
    serializer_class = ebookSerializer


# Create your views here.

# GET/POST

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def base(request):
    return render(request, '../templates/scribd/base.html')


def add_books_form(request):
    return render(request, '../templates/forms/add_book.html')


# ------------------------------------------User management------------------------------------------------

def logout_create_view(request):
    return redirect('mainpage')

def login_create_view(request):
    if request.method == "POST":
        login_form = AuthenticationForm(None, data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('mainpage')
    else:

        login_form = AuthenticationForm()

    return render(request, '../templates/registration/login.html', {'form': login_form})


def signup_create_view(request):
    if request.method == 'POST':

        signup_form = RegisterForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = User.objects.create_user(email = signup_form.cleaned_data.get('email'),
                username=signup_form.cleaned_data.get('username'),
                first_name=signup_form.cleaned_data.get('first_name'),
                last_name="",
                type=signup_form.cleaned_data.get('type'),
                password=signup_form.cleaned_data.get('password1'))
            print(user.type)
            login(request, user)
            return redirect('mainpage')
    else:
        print(request)
        signup_form = RegisterForm()
    return render(request, '../templates/registration/signup.html', {'form': signup_form})


'''


 user = UserManager.create_user(
                email = signup_form.cleaned_data.get('email'),
                username=signup_form.cleaned_data.get('username'),
                first_name=signup_form.cleaned_data.get('first_name'),
                last_name="",
                password=signup_form.cleaned_data.get('password1'))


user = signup_form.save(commit=False)
            #user.refresh_from_db()
            user.username = signup_form.cleaned_data.get('username')
            user.set_password(signup_form.cleaned_data.get('password1'))
            user.email = signup_form.cleaned_data.get('email')
            user.date_registration = datetime.now().date()
            user.subscription = True
            user.type = 'subscribed'
            user.save()
            raw_password = signup_form.cleaned_data.get('password1')
            #user = authenticate(username=user.username, password=raw_password)
            print(user)

'''