import json

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from rest_framework import generics, viewsets, permissions

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import user_passes_test
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer, TemplateHTMLRenderer
from Scribd.forms import EbookForm, RegisterForm, CreditCardForm
from Scribd.user_model import User, UserManager, SubscribedUsers
from Scribd.forms import EbookForm, RegisterForm, TicketForm, ProfileForm, UpgradeAccountForm, UploadFileForm
from requests import Response
from Scribd.models import Ebook, UserTickets, UploadedResources
from Scribd.permissions import EditBookPermissions
from Scribd.serializers import UserSerializer, EbookSerializer, ticketSerializer, UploadResourcesSerializer
from Scribd.user_model import User


def provider_page(request):
    return render(request, 'scribd/providers_homepage.html')


def support_page(request):
    return render(request, 'scribd/support_page.html')


def ebook_search(request, title="", category="", media_type=""):
    if title or category or media_type:
        if title:
            ebooks_ = Ebook.objects.filter(title__iexact=title)
        if category:
            ebooks_ = Ebook.objects.filter(category__iexact=category).order_by('category')
        if media_type:
            ebooks_ = Ebook.objects.filter(media_type__iexact=media_type)
    else:
        ebooks_ = Ebook.objects.all()

    if request.method == "GET":
        dictionary = request.GET.dict()
        token = dictionary.get("category")
        if token:
            ebooks_by_category = Ebook.objects.filter(category__iexact=category)
    context = {
        'tittle': title,
        'category': category,
        'ebooks': ebooks_,
    }
    return render(request, 'Scribd/ebooks_list.html', context)


def ticket_page(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket_form.save()
            return redirect('mainpage')
    else:
        ticket_form = TicketForm()

    return render(request, 'scribd/tickets.html', {'ticket_form': ticket_form})

  
def base(request):
    return render(request, 'scribd/base.html')
  
  
def ebook_create_view(request):
    if request.method == 'POST':
        form = EbookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            instance = form.save(commit=False)
            print(instance.featured_photo)
            form.save()
            return redirect('mainpage')
    else:
        form = EbookForm()
    return render(request, 'forms/add_book.html', {'book_form': form})


'''
def support_group(user):
    return 'support' in user.groups
'''

#@user_passes_test(support_group)
class ticketListView(ListView):
    model = UserTickets
    template_name = 'scribd/support_page.html'    

class ticketViewSet(viewsets.ModelViewSet):
    queryset = UserTickets.objects.all().order_by('id_uTicket')
    serializer_class = ticketSerializer

    def get_queryset(self):
        return UserTickets.objects.all().order_by('id')

class ebookMainView(ListView):
    model = Ebook
    template_name = 'scribd/mainpage.html'


class ebookListView(ListView):
    model = Ebook
    template_name = 'scribd/ebooks_list.html'


class ebookDetailView(DetailView):
    model = Ebook
    template_name = 'scribd/ebook_detail.html'


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


def add_books_form(request):
    return render(request, 'forms/add_book.html')


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('date_registration')
    serializer_class = UserSerializer

    # permission_classes = permissions.IsAuthenticatedOrReadOnly

    def get_queryset(self):
        return User.objects.all().order_by('date_registration')


def login_create_view(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == "POST":
        login_form = AuthenticationForm(None, data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user, backend)
            if user.user_type == "Provider":
                return redirect('provider_page')
            elif user.user_type == "Support":
                return redirect('support_page')
            elif user.user_type == "Admin":
                return HttpResponseRedirect(reverse('admin:index'))
            return redirect('mainpage')

    else:

        login_form = AuthenticationForm()

    return render(request, 'scribd/base.html', {'login_form': login_form})


def signup_create_view(request,backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == 'POST':

        signup_form = RegisterForm(request.POST, request.FILES)
        credit_form = CreditCardForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = User.objects.create_user(
            email=signup_form.cleaned_data.get('email'),
            username=signup_form.cleaned_data.get('username'),
            first_name=signup_form.cleaned_data.get('first_name'),
            last_name=signup_form.cleaned_data.get('last_name'),
            password=signup_form.cleaned_data.get('password1'),
            subs_type = signup_form.cleaned_data.get('subs_type'))
            user.save()
            if credit_form.is_valid():
                user = User.objects.get(username=user.username)
                credit_form.instance.username = user
                card_titular = credit_form.cleaned_data.get('card_titular'),
                card_number = credit_form.cleaned_data.get('card_number'),
                card_expiration = credit_form.cleaned_data.get('card_expiration'),
                card_cvv = credit_form.cleaned_data.get('card_cvv')
                credit_form.save()

            login(request, user, backend)
            if user.user_type == "Provider":
                return redirect('provider_page')
            elif user.user_type == "Support":
                return redirect('support_page')
            elif user.user_type == "Admin":
                return HttpResponseRedirect(reverse('admin:index'))
            return redirect('mainpage')
    else:

        signup_form = RegisterForm()
        credit_form = CreditCardForm()

    context = {
        "register_form": signup_form,
        "credit_form": credit_form
    }
    return render(request, 'registration/signup.html', context)


class BookUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, EditBookPermissions) # NOT WORKING
    queryset = Ebook.objects.all()
    serializer_class = EbookSerializer
    template_name = 'scribd/ebook_change.html'
    form_class = EbookForm

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.title = request.data.get("title")
        instance.autor = request.data.get("autor")
        instance.description = request.data.get("description")
        instance.is_promot = request.data.get("is_promot")
        instance.featured_photo = request.data.get("featured_photo")
        instance.category = request.data.get("category")
        instance.media_type = request.data.get("media_type")
        instance.count_downloads = request.data.get("count_downloads")
        instance.url = request.data.get("url")
        instance.save()

        serializer = EbookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

      
class user_profile_page(DetailView):
    model = User
    template_name = 'scribd/user_profile_page_notworking.html'


def edit_profile_page(request, pk):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('mainpage')
    else:
        form = ProfileForm(instance=request.user)
    context = {
        "form": form
    }
    return render(request, 'forms/edit_user_profile.html', context)


def upgrade_account_view(request, pk):
    if request.method == "POST":
        form = UpgradeAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            user = User.objects.get(username=pk)
            if user.subs_type == "Free trial":
                user.nbooks_by_subs = 10
            if user.subs_type == "Regular":
                user.nbooks_by_subs = 100
            if user.subs_type == "Pro":
                user.nbooks_by_subs = 1000

            user.save()

            return redirect('mainpage')
    else:
        form = UpgradeAccountForm(instance=request.user)

    context = {
        "form": form
    }

    return render(request, 'forms/upgrade_account.html', context)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            print(instance.user.uploadedresources_set.all())
            form.save()
            return redirect('mainpage')
    else:
        form = UploadFileForm()
    return render(request, 'forms/upload.html', {'upload_file_form': form})


class UploadsViewSet(viewsets.ModelViewSet):
    queryset = UploadedResources.objects.all().order_by('id')
    serializer_class = UploadResourcesSerializer

    # permission_classes = permissions.IsAuthenticatedOrReadOnly

    def get_queryset(self):
        return UploadedResources.objects.all().order_by('id')

      
#@user_passes_test(support_group)
def change_ebook(request, pk):
    instance = Ebook.objects.get(pk=pk)
    form = EbookForm(request.POST or None, instance=instance)
    if form.is_valid():
          form.save()
          return redirect('mainpage')
    return render(request, 'scribd/ebook_change.html', {'form': form})
