import datetime

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from requests import Response
from rest_framework import generics, viewsets, permissions

from Scribd.decorators import allowed_users, authentificated_user
from Scribd.forms import EbookForm, RegisterForm, TicketForm, ProfileForm, UploadFileForm, \
    FollowForm, ProfileFormProvider, Subscription, CancelSubscription, UpgradeAccountForm, UpdatePayment, \
    CreateInForum, CreateInDiscussion, CreateInDiscussionTicket, ReviewForm
from Scribd.models import ViewedEbooks, Review, Discussion, DiscussionTickets
from Scribd.permissions import EditBookPermissions
from Scribd.serializers import *
from .user_models import User, userProfile, providerProfile


##################################
####### VISTA MAINPAGE ###########
##################################

def base(request):
    return render(request, 'scribd/base.html')


def index(request):
    ebooks = Ebook.objects.all()
    paginator = Paginator(ebooks, 3)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidrPage):
        posts = paginator.page(paginator.num_pages)
    # Get the index of the current page
    index = posts.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]
    promoted = True
    context = {
        'ebooks': posts,
        'promoted': promoted,
        'page_range': page_range,
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
    instance2 = providerProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = EbookForm(request.POST, request.FILES)
        if form.is_valid():
            ebook = Ebook.objects.create(
                ebook_number=form.cleaned_data.get('ebook_number'),
                title=form.cleaned_data.get('title'),
                autor=form.cleaned_data.get('autor'),
                description=form.cleaned_data.get('description'),
                size=form.cleaned_data.get('size'),
                media_type=form.cleaned_data.get('media_type'),
                # featured_photo=form.cleaned_data.get('featured_photo'),
                publisher=instance2,
            )
            ebook.save()
            return redirect('index')
    else:
        form = EbookForm()
    books = []
    for book in Ebook.objects.all():
        if str(book.publisher)[21:] == instance2.publisher:
            books.append(book)
    return render(request, 'scribd/providers_homepage.html',
                  {'book_form': form, 'provider_instance': instance2, 'books': books})


##################################
####### VISTA REVIEW #############
##################################


##################################
####### VISTA LOGIN ##############
##################################

def login_create_view(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == "POST":
        login_form = AuthenticationForm(None, data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user, backend)
            request.session['login'] = True
            if user.is_provider:
                return redirect('provider_page')
            elif user.is_support:
                return redirect('support_page')
            elif user.is_provider:
                return HttpResponseRedirect(reverse('admin:index'))
            return redirect('index')
        else:
            request.session['login'] = False
            return redirect('index')

    else:
        login_form = AuthenticationForm()

    return render(request, 'scribd/mainpage.html', {'login_form': login_form})


##################################
####### VISTA REGISTRO ###########
##################################

def signup_create_view(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == 'POST':
        signup_form = RegisterForm(request.POST, request.FILES)
        user = None
        if signup_form.is_valid():
            user = User.objects.create_user(
                email=signup_form.cleaned_data.get('email'),
                username=signup_form.cleaned_data.get('username'),
                first_name=signup_form.cleaned_data.get('first_name'),
                last_name=signup_form.cleaned_data.get('last_name'),
                password=signup_form.cleaned_data.get('password1'))

            userprofile = userProfile.objects.create(user=user)
            userprofile.subs_type = "Free trial"
            userprofile.nbooks_by_subs = 10
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
            messages.error(request, "Error")
            return redirect('index')

    else:
        signup_form = RegisterForm()
        context = {
            "register_form": signup_form,
        }
        return render(request, 'registration/signup.html', context)


@csrf_exempt
def update_session(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    request.session['login'] = None
    return HttpResponse('ok')


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
    return render(request, 'forms/edit_user_profile_v2.html', context)


class user_profile_page(DetailView):
    template_name = 'scribd/user_profile_page.html'
    model = userProfile

    def get_object(self):
        UserName = self.kwargs.get("username")
        return get_object_or_404(User, username=UserName)

    def get_context_data(self, **kwargs):
        context = super(user_profile_page, self).get_context_data(**kwargs)
        current_time = datetime.datetime.now()
        user = self.get_object()
        substract = user.user_profile.nbooks_by_subs - user.user_profile.n_books_followed
        context['current_time'] = current_time
        context['substract'] = substract
        return context


@allowed_users(allowed_roles=['provider'])
def provider_page(request):
    return render(request, 'scribd/providers_homepage.html')


def contract_page(request):
    return render(request, 'scribd/contract.html')


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
        form_subs = Subscription(request.POST, instance=request.user.user_profile)
        user = User.objects.get(username=username)
        prev_state = user.user_profile.subs_type
        if form.is_valid() and form_subs.is_valid():
            form.save()
            form_subs.save()
            user = User.objects.get(username=username)

            # If user cancel subscription...
            if user.user_profile.subs_type == "Free trial":
                # If has more than 10 books followed we must display the correct value
                if user.user_profile.n_books_followed >= 10:
                    user.user_profile.n_books_followed = 10
                user.user_profile.nbooks_by_subs = 10

            # if user upgrade to regular but it's the first time then he/she has 50 books to read
            if user.user_profile.subs_type == "Regular":
                if user.user_profile.first_upgrade or prev_state == "Free trial":
                    user.user_profile.first_upgrade = False  # html
                    user.user_profile.nbooks_by_subs = 50
                # otherwise, we add 20 new books
                else:
                    user.user_profile.nbooks_by_subs += 20

            # if user upgrade to pro but it's the first time then he/she has 100 books to read
            if user.user_profile.subs_type == "Pro":
                if user.user_profile.first_upgrade or prev_state == "Free trial":
                    user.user_profile.first_upgrade = False  # html
                    user.user_profile.nbooks_by_subs = 100
                # otherwise, we add 50 new books
                else:
                    user.user_profile.nbooks_by_subs += 50
            user.user_profile.expires = datetime.datetime.now() + datetime.timedelta(weeks=4)
            user.user_profile.save()
            return redirect('userprofilepage', username=username)
    else:
        form = UpgradeAccountForm(instance=request.user.user_profile)
        form_subs = Subscription(instance=request.user.user_profile)
        context = {
            "form": form,
            "current_time": datetime.datetime.now(),
            "form_subs": form_subs
        }

        return render(request, 'forms/upgrade_account.html', context)


def downgrade_account_view(request, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        if user.user_profile.subs_type == "Regular" or user.user_profile.subs_type == "Pro":
            # downgrade to Free trial user
            user.user_profile.subs_type = "Free trial"
            user.user_profile.nbooks_by_subs = 10
            # If has more than 10 books followed we must display the correct value
            if user.user_profile.n_books_followed >= 10:
                user.user_profile.n_books_followed = 10
            # If now change the value displayed
            else:
                user.user_profile.n_books_followed = user.user_profile.n_books_followed

        user.user_profile.expires = datetime.datetime.now()
        user.user_profile.save()
        return redirect('userprofilepage', username=username)
    else:
        form = CancelSubscription(instance=request.user.user_profile)
        context = {
            "form": form,
        }
        return render(request, 'forms/cancel_subscription_confirmation_v2.html', context)


@authentificated_user
def update_payment_details(request, username):
    credit_form = Subscription(request.POST or None, request.FILES)
    if request.method == "POST":
        form = UpdatePayment(request.POST, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=username)
            if credit_form.is_valid():
                user.user_profile.card_titular = credit_form.cleaned_data.get('card_titular'),
                user.user_profile.card_number = credit_form.cleaned_data.get('card_number'),
                user.user_profile.card_expiration = credit_form.cleaned_data.get('card_expiration'),
                user.user_profile.card_cvv = credit_form.cleaned_data.get('card_cvv')

                user.user_profile.save()
                return redirect('userprofilepage', username=username)
    else:
        form = UpgradeAccountForm(instance=request.user.user_profile)
        credit_form = Subscription()

    context = {
        "form": form,
        "credit_form": credit_form
    }

    return render(request, 'forms/update_payment.html', context)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print("estoy aqui PAYASO")
        if form.is_valid():
            print("EL FORM ES VALIDO")
            instance = form.save(commit=False)
            instance.user = request.user
            instance.user.user_profile.n_uploads += 1
            instance.user.user_profile.save()
            form.save()
            return redirect('index')
    else:
        print("EL FORM NO ES VALIDO")
        form = UploadFileForm()
    return render(request, 'forms/upload.html', {'upload_file_form': form})


def follow(request, pk):
    if request.method == 'POST':
        if 'follow' in request.POST:

            form = FollowForm(request.POST)
            if form.is_valid():
                user = request.user

                # always update the value. Controlled in front-end
                print(list(user.users_key.values()))
                user.user_profile.n_books_followed += 1
                user.user_profile.save()

                instance = Ebook.objects.get(id=pk)
                instance.follower.add(user)
                instance.save()
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)
        elif 'create_forum' in request.POST:

            forum_form = CreateInForum(request.POST)

            if forum_form.is_valid() and request.user.is_authenticated:
                forum = Forum.objects.create(
                    ebook=Ebook.objects.get(id=pk),
                    user=request.user,
                    email=request.user.email,
                    topic=forum_form.cleaned_data.get('topic'),
                    description=forum_form.cleaned_data.get('description'),
                    link=forum_form.cleaned_data.get('link'),

                )
                forum.save()
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)

        elif 'review' in request.POST:
            print(request.POST)
            review_form = ReviewForm(request.POST)

            if review_form.is_valid() and request.user.is_authenticated:
                review = Review.objects.create(
                    ebook=Ebook.objects.get(id=pk),
                    comment=review_form.cleaned_data.get("comment"),
                    value_stars=review_form.cleaned_data.get("value_stars"),
                    user=request.user
                )
                review.save()

            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        else:
            print(request.POST)
            print("There was a problem with this post bro")
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    else:
        discussion_form = CreateInDiscussion()
        review_form = ReviewForm
        forum_form = CreateInForum()
        form = FollowForm()
        ebook = Ebook.objects.get(id=pk)
        forums = ebook.forum_set.all()
        count = forums.count()
        discussions = []
        for i in forums:
            discussions.append(i.discussion_set.all())

        reviews = Review.objects.filter(ebook=ebook)
        if request.user.is_authenticated:
            if request.user.is_provider or request.user.is_provider or request.user.is_superuser:
                context = {
                    "form": form,
                    "ebook": ebook,
                    "review_form": review_form,
                    "reviews": reviews,
                    "discussion_form": discussion_form,
                    "create_forum": forum_form,
                    'forums': ebook.forum_set.all(),
                    'count': count,
                    'discussions': discussions
                }
            else:
                followed = False
                for e in list(request.user.users_key.values()):
                    if e['id'] == ebook.id:
                        followed = True

                context = {
                    "form": form,
                    "substract": request.user.user_profile.nbooks_by_subs - request.user.user_profile.n_books_followed,
                    "ebook_followed": followed,
                    "ebook": ebook,
                    "review_form": review_form,
                    "reviews": reviews,
                    "discussion_form": discussion_form,
                    "create_forum": forum_form,
                    'forums': ebook.forum_set.all(),
                    'count': count,
                    'discussions': discussions
                }
        else:
            context = {
                "reviews": reviews,
                "discussion_form": discussion_form,
                "create_forum": forum_form,
                "review_form": review_form,
                "form": form,
                "ebook": ebook,
                'forums': ebook.forum_set.all(),
                'count': count,
                'discussions': discussions
            }

        return render(request, 'scribd/ebook_details.html', context)


def ebook_forum(request, book_k, forum_k):
    if request.method == 'POST':
        discussion_form = CreateInDiscussion(request.POST)

        if discussion_form.is_valid() and request.user.is_authenticated:
            discussion = Discussion.objects.create(
                user=request.user,
                forum=Forum.objects.get(id=forum_k),
                discuss=discussion_form.cleaned_data.get("discuss"),
            )

            discussion.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    else:

        discussion_form = CreateInDiscussion()
        forum = Forum.objects.get(id=forum_k)
        discussions = forum.discussion_set.all()
        context = {
            'forum': forum,
            'discussion_form': discussion_form,
            'discuss': discussions
        }

        return render(request, 'scribd/forumdetail.html', context)


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


def ticket_page(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = UserTickets.objects.create(
                ticket_title=ticket_form.cleaned_data.get('ticket_title'),
                ticket_summary=ticket_form.cleaned_data.get('ticket_summary'),
                ticket_user=User.objects.get(username=request.user.username),

            )
            ticket.save()

            return redirect('index')
    else:
        ticket_form = TicketForm()

    return render(request, 'scribd/tickets.html', {'ticket_form': ticket_form})


def ticketForumView(request, pk):
    if request.method == 'POST':
        discussion_form = CreateInDiscussionTicket(request.POST)

        if discussion_form.is_valid() and request.user.is_authenticated:
            discussion = DiscussionTickets.objects.create(
                user=User.objects.get(id=User.objects.get(username=request.user.username).id),
                userticket=UserTickets.objects.get(id_uTicket=pk),
                discuss=discussion_form.cleaned_data.get("discuss")
            )

            discussion.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    else:

        discussion_form = CreateInDiscussionTicket()
        ticket = UserTickets.objects.get(id_uTicket=pk)
        discussions = ticket.discussiontickets_set.all()
        context = {
            'ticket': ticket,
            'discussion_form': discussion_form,
            'discuss': discussions
        }

        return render(request, 'scribd/ticketdetail.html', context)


@authentificated_user
def support_page(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = UserTickets.objects.create(
                ticket_title=ticket_form.cleaned_data.get('ticket_title'),
                ticket_summary=ticket_form.cleaned_data.get('ticket_summary'),
                ticket_user=User.objects.get(username=request.user.username),

            )
            ticket.save()

            return redirect('support_page')
    else:
        ticket_form = TicketForm()
        tickets = UserTickets.objects.all()
        context = {
            'tickets': tickets,
            'ticket_form': ticket_form
        }
        return render(request, 'scribd/support_page.html', context)


##################################
####### VISTA EBOOK ##############
##################################

def add_books_form(request):
    return render(request, 'forms/add_book.html')


class ebookListView(ListView):
    model = Ebook
    template_name = 'scribd/ebooks_list.html'


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


@allowed_users(allowed_roles=['support'])
def change_ebook(request, pk):
    instance = Ebook.objects.get(pk=pk)
    form = EbookForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'scribd/ebook_change.html', {'form': form})


##################################
####### VISTA FORUM ##############
##################################

class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all().order_by('date_created')
    serializer_class = ForumSerializer

    # permission_classes = permissions.IsAuthenticatedOrReadOnly

    def get_queryset(self):
        return User.objects.all().order_by('date_created')
