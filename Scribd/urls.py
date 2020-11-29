from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

from Scribd import views
from Scribd.views import UserList, UserDetail
from Scribd.views import ebook_create_view, ebookListView, signup_create_view, login_create_view, \
    provider_page, edit_profile_page_provider, contract_page, review, \
    ticket_page, user_profile_page, edit_profile_page, upgrade_account_view, upload_file, ticketListView, follow, \
    downgrade_account_view, support_page
from ScribdProject import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^base/$', views.base, name='base'),
    url(r'^ebooks/$', views.ebooks, name='ebooks'),
    url(r'^ebooks/(?P<category>.*)/$', views.ebooks, name='ebooks'),

    url('ebookdetail/(?P<pk>[0-9]+)/$', follow, name='ebook_custom_detail'),
    url('changebook/(?P<pk>[0-9]+)/$', views.change_ebook, name='Ebook_change_details'),
    
    url('review/(?P<pk>[0-9]+)/$', review, name='review'),

    url('upload_file/', upload_file, name='upload_file'),
    
    url('accounts/login/', login_create_view, name='login'),
    url('accounts/signup/', signup_create_view, name='signup'),

    url('provider/', provider_page, name='provider_page'), #only self provider!!!!!
    url('contract/', contract_page, name='contract_page'), #only self provider!!!!!
    url('addbook/', ebook_create_view, name='add_book'),

    url('ticket/', ticket_page, name='ticket_page'),
    url('supportPage/', support_page, name='support_page'),

    url('profile/(?P<username>\w+)/$', user_profile_page.as_view(), name='userprofilepage'), #only self
    url('profile/(?P<username>\w+)/edit/$', edit_profile_page, name='edituserprofile'), #only self
    url('profile/(?P<username>\w+)/upgrade/$', upgrade_account_view, name='upgradeaccount'), #only self

    url('User/$', UserList.as_view()),
    url('User/(?P<username>\w+)/$', UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
# urlpatterns += staticfiles_urlpatterns()
urlpatterns += [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
