from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from requests import Response
from rest_framework import generics, viewsets, permissions

from Scribd.forms import EbookForm, RegisterForm, TicketForm, ProfileForm, UploadFileForm, \
    FollowForm, ProfileFormProvider, Subscription, UpgradeAccountForm
from Scribd.models import Ebook, UserTickets, UploadedResources, ViewedEbooks
from Scribd.permissions import EditBookPermissions
from Scribd.serializers import UserSerializer, EbookSerializer, ticketSerializer, UploadResourcesSerializer
from .user_models import User, userProfile


##################################
####### VISTA MAINPAGE ###########
##################################

def base(request):
    return render(request, 'scribd/base.html')

def index(request):
    ebooks = Ebook.objects.all()
    promoted = True
    context = {
        'ebooks': ebooks,
        'promoted': promoted,
        'viewedebooks': _check_session(request)
    }
    return render(request, 'scribd/mainpage.html', context)


def _check_session(request):
    if "viewedebooks" not in request.session:
        viewedebooks = ViewedEbooks()
        viewedebooks.save()
        request.session["viewedebooks"] = viewedebooks.id_vr
    else:
        viewedebooks = ViewedEbooks.objects.get(id_vr=request.session["viewedebooks"])
    return viewedebooks


class ebookMainView(ListView):
    model = Ebook
    template_name = 'scribd/mainpage.html'
    
def ebooks(request, search=""):
    # Priorizamos busqueda categoria
    if request.method == "GET":
        dictionary = request.GET.dict()
        query = dictionary.get("search")
        if query:
            ebooks = Ebook.objects.filter(
                Q(ebook_number__icontains=query) |
                Q(title__icontains=query) |
                Q(autor__icontains=query) |
                Q(description__icontains=query) |
                Q(is_promot__icontains=query) |
                Q(size__icontains=query) |
                Q(category__icontains=query) |
                Q(media_type__icontains=query) |
                Q(featured_photo__icontains=query) |
                Q(url__icontains=query)
            )
        else:
            ebooks = Ebook.objects.all()

    else:
        ebooks = Ebook.objects.all()

    context = {
        'search': search,
        'ebooks': ebooks,
        'viewedebooks': _check_session(request)
    }
    return render(request, 'scribd/mainpage.html', context)


def ebook_create_view(request):
    if request.method == 'POST':
        form = EbookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            instance = form.save(commit=False)
            print(instance.featured_photo)
            form.save()
            return redirect('index')
    else:
        form = EbookForm()
    return render(request, 'forms/add_book.html', {'book_form': form})


##################################
####### VISTA TICKET #############
##################################

def ticket_page(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket_form.save()
            return redirect('index')
    else:
        ticket_form = TicketForm()

    return render(request, 'scribd/tickets.html', {'ticket_form': ticket_form})


##################################
####### VISTA LOGIN ###########
##################################

def login_create_view(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == "POST":
        login_form = AuthenticationForm(None, data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user, backend)

            if user.is_provider:
                return redirect('provider_page')
            elif user.is_support:
                return redirect('support_page')
            elif user.is_provider:
                return HttpResponseRedirect(reverse('admin:index'))
            return redirect('index')

    else:

        login_form = AuthenticationForm()

    return render(request, 'scribd/base.html', {'login_form': login_form})


##################################
####### VISTA REGISTRO ###########
##################################

# TODO HAY UN BUG EN EL SEGUNDO FORMULARIO

def signup_create_view(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == 'POST':
        signup_form = RegisterForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = User.objects.create_user(
                email=signup_form.cleaned_data.get('email'),
                username=signup_form.cleaned_data.get('username'),
                first_name=signup_form.cleaned_data.get('first_name'),
                last_name=signup_form.cleaned_data.get('last_name'),
                password=signup_form.cleaned_data.get('password1'))
            credit_form = Subscription(request.POST or None, request.FILES)
            if credit_form.is_valid():
                userprofile = userProfile.objects.create(user=user)
                userprofile.subs_type = credit_form.cleaned_data.get('subs_type'),
                print(credit_form.cleaned_data.get('subs_type'))
                if userprofile.subs_type == "Free trial":
                    userprofile.nbooks_by_subs = 10
                if userprofile.subs_type == "Regular":
                    userprofile.nbooks_by_subs = 100
                if userprofile.subs_type == "Pro":
                    userprofile.nbooks_by_subs = 1000
                userprofile.card_titular = credit_form.cleaned_data.get('card_titular'),
                print(credit_form.cleaned_data.get('card_titular'))
                userprofile.card_number = credit_form.cleaned_data.get('card_number'),
                userprofile.card_expiration = credit_form.cleaned_data.get('card_expiration'),
                userprofile.card_cvv = credit_form.cleaned_data.get('card_cvv')
                userprofile.save()

            login(request, user, backend)
            if user.is_provider:
                return redirect('provider_page')
            elif user.is_support:
                return redirect('support_page')
            elif user.is_provider:
                return HttpResponseRedirect(reverse('admin:index'))
            return redirect('index')
    else:

        signup_form = RegisterForm()
        credit_form = Subscription()

    context = {
        "register_form": signup_form,
        "credit_form": credit_form
    }
    return render(request, 'registration/signup.html', context)


##################################
####### VISTA PROFILE ###########
##################################

def edit_profile_page_provider(request):
    if request.method == "POST":
        form = ProfileFormProvider(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProfileFormProvider(instance=request.user)
    context = {
        "form": form
    }
    return render(request, 'forms/edit_provider_profile.html', context)


def edit_profile_page(request, username):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return redirect('userprofilepage', username=username)
    else:
        form = ProfileForm(instance=request.user.user_profile)
    context = {
        "form": form
    }
    return render(request, 'forms/edit_user_profile.html', context)


class user_profile_page(DetailView):
    template_name = 'scribd/user_profile_page.html'
    model = userProfile

    def get_object(self):
        UserName = self.kwargs.get("username")
        return get_object_or_404(User, username=UserName)


def provider_page(request):
    return render(request, 'scribd/providers_homepage.html')


def contract_page(request):
    return render(request, 'scribd/contract.html')


def support_page(request):
    return render(request, 'scribd/support_page.html')


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    # permission_classes = permissions.IsAuthenticatedOrReadOnly

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        UserName = self.kwargs.get("username")
        return get_object_or_404(User, username=UserName)


##################################
####### UPGRADE AND FILES ########
##################################

def upgrade_account_view(request, username):
    if request.method == "POST":
        form = UpgradeAccountForm(request.POST, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=username)
            if user.user_profile.subs_type == "Free trial":
                user.user_profile.nbooks_by_subs = 10
            if user.user_profile.subs_type == "Regular":
                user.user_profile.nbooks_by_subs = 100
            if user.user_profile.subs_type == "Pro":
                user.user_profile.nbooks_by_subs = 1000
            user.user_profile.save()
            return redirect('userprofilepage', username=username)
    else:
        form = UpgradeAccountForm(instance=request.user.user_profile)

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
            return redirect('index')
    else:
        form = UploadFileForm()
    return render(request, 'forms/upload.html', {'upload_file_form': form})


def follow(request, pk):
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            user = request.user
            n_books_left = user.user_profile.nbooks_by_subs
            if n_books_left > 0:
                user.user_profile.nbooks_by_subs -= 1
                user.user_profile.save()
            instance = Ebook.objects.get(id=pk)
            instance.follower = user
            instance.save()
            return redirect('index')
    else:
        form = FollowForm()
        ebook = Ebook.objects.get(id=pk)
        context = {
            "form": form,
            "ebook": ebook
        }
    return render(request, 'scribd/ebook_detail.html', context)


class UploadsViewSet(viewsets.ModelViewSet):
    queryset = UploadedResources.objects.all().order_by('id')
    serializer_class = UploadResourcesSerializer

    # permission_classes = permissions.IsAuthenticatedOrReadOnly

    def get_queryset(self):
        return UploadedResources.objects.all().order_by('id')


##################################
####### VISTA TICKETS ############
##################################

class ticketListView(ListView):
    model = UserTickets
    template_name = 'scribd/support_page.html'


class ticketViewSet(viewsets.ModelViewSet):
    queryset = UserTickets.objects.all().order_by('id_uTicket')
    serializer_class = ticketSerializer

    def get_queryset(self):
        return UserTickets.objects.all().order_by('id')


##################################
####### VISTA EBOOK ##############
##################################

def add_books_form(request):
    return render(request, 'forms/add_book.html')


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


class BookUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, EditBookPermissions)  # NOT WORKING
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


def change_ebook(request, pk):
    instance = Ebook.objects.get(pk=pk)
    form = EbookForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'scribd/ebook_change.html', {'form': form})
