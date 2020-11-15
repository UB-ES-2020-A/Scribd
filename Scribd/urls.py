from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns

from Scribd import views
from Scribd.views import UserList, UserDetail, BookUpdateView
from Scribd.views import ebook_create_view, ebookListView, ebookDetailView, signup_create_view, login_create_view, \
    provider_page, ebookMainView, ticket_page, user_profile_page, edit_profile_page
from ScribdProject import settings

urlpatterns = [
    url(r'^$', ebookMainView.as_view(), name='mainpage'),
    url(r'^base/$', views.base, name='base'),
    url('ebooklist/', ebookListView.as_view(), name='ebook_custom_list'),
    url('ebookdetail/(?P<pk>[0-9]+)/$', ebookDetailView.as_view(), name='ebook_custom_detail'),
    url('changebook/(?P<pk>[0-9]+)/$', BookUpdateView.as_view(), name='Ebook_change_details'),
    url('addbook/', ebook_create_view, name='add_book'),
    url('User/$', UserList.as_view()),
    url('User/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url('userprofile/(?P<pk>[a-zA-Z0-9]+)/$', user_profile_page.as_view(), name='userprofilepage'),
    url('userprofile/(?P<pk>[a-zA-Z0-9]+)/edit/$', edit_profile_page, name='edituserprofile'),
    url('accounts/login/', login_create_view, name='login'),
    url('accounts/signup/', signup_create_view, name='signup'),
    url('provider/', provider_page, name='provider_page'),
    url('ticket/', ticket_page, name='ticket_page'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
#urlpatterns += staticfiles_urlpatterns()
urlpatterns += [
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)