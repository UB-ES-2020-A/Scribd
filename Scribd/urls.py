from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

from Scribd import views
from Scribd.views import ebookListView, follow, ebook_create_view, edit_profile_page_provider, UserList, UserDetail, \
    user_profile_page, edit_profile_page, upgrade_account_view, upload_file, login_create_view, signup_create_view, \
    provider_page, contract_page, ticket_page, ticketForumView, support_page
from ScribdProject import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^base/$', views.base, name='base'),
    url(r'^ebooks/$', views.ebooks, name='ebooks'),
    url(r'^ebooks/(?P<category>.*)/$', views.ebooks, name='ebooks'),

    url('ebooklist/', ebookListView.as_view(), name='ebook_custom_list'),
    url('ebookdetail/(?P<pk>[0-9]+)/$', follow, name='ebook_custom_detail'),
    url('changebook/(?P<pk>[0-9]+)/$', views.change_ebook, name='Ebook_change_details'),
    url('addbook/', ebook_create_view, name='add_book'),
    url('provider/edit/$', edit_profile_page_provider, name='edituserprofileprovider'),
    url('User/$', UserList.as_view()),
    url('User/(?P<username>\w+)/$', UserDetail.as_view()),
    url('profile/(?P<username>\w+)/$', user_profile_page.as_view(), name='userprofilepage'),
    url('profile/(?P<username>\w+)/edit/$', edit_profile_page, name='edituserprofile'),
    url('profile/(?P<username>\w+)/upgrade/$', upgrade_account_view, name='upgradeaccount'),
    url('upload_file/', upload_file, name='upload_file'),
    url('accounts/login/', login_create_view, name='login'),
    url('accounts/signup/', signup_create_view, name='signup'),
    url('provider/', provider_page, name='provider_page'),
    url('contract/', contract_page, name='contract_page'),
    url('ticket/', ticket_page, name='ticket_page'),
    url('ticketdetail/(?P<pk>[0-9]+)/$', ticketForumView, name='ticketdetail'),
    url('supportPage/', support_page, name='support_page'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
# urlpatterns += staticfiles_urlpatterns()
urlpatterns += [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
