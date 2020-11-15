from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from ScribdProject import settings
from Scribd import views
from Scribd.views import UserList, UserDetail, BookUpdateView
from Scribd.views import ebook_create_view, ebookListView, ebookDetailView, signup_create_view, login_create_view, \
    provider_page, ebookMainView, edit_profile_page_provider, contract_page, \
    ticket_page, user_profile_page, edit_profile_page, upgrade_account_view, upload_file, ticketListView, follow

urlpatterns = [
    url(r'^$', ebookMainView.as_view(), name='mainpage'),
    url(r'^base/$', views.base, name='base'),
    url('ebooklist/', ebookListView.as_view(), name='ebook_custom_list'),
    url(r'^ebooklist/(?P<category>.*)/$', views.ebook_search, name='ebook_search'),
    url('ebookdetail/(?P<pk>[0-9]+)/$', follow, name='ebook_custom_detail'),
    url('changebook/(?P<pk>[0-9]+)/$', views.change_ebook, name='Ebook_change_details'),
    url('addbook/', ebook_create_view, name='add_book'),
    url('provider/edit/$', edit_profile_page_provider, name='edituserprofileprovider'),
    url('User/$', UserList.as_view()),
    url('User/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url('userprofile/(?P<pk>[a-zA-Z0-9]+)/$', user_profile_page.as_view(), name='userprofilepage'),
    url('userprofile/(?P<pk>[a-zA-Z0-9]+)/edit/$', edit_profile_page, name='edituserprofile'),
    url('userprofile/(?P<pk>[a-zA-Z0-9]+)/upgrade/$', upgrade_account_view, name='upgradeaccount'),
    url('upload_file/', upload_file, name='upload_file'),
    url('accounts/login/', login_create_view, name='login'),
    url('accounts/signup/', signup_create_view, name='signup'),
    url('provider/', provider_page, name='provider_page'),
    url('contract/', contract_page, name='contract_page'),
    url('ticket/', ticket_page, name='ticket_page'),
    url('supportPage/', ticketListView.as_view(), name='support_page'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
#urlpatterns += staticfiles_urlpatterns()
urlpatterns += [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)