from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

from Scribd import views
from Scribd.views import follow, ebook_create_view, user_profile_page, edit_profile_page, upgrade_account_view, \
    upload_file, login_create_view, signup_create_view, \
    provider_page, contract_page, ticket_page, ticketForumView, support_page, update_payment_details, \
    downgrade_account_view, UserList, UserDetail,ebook_forum
from ScribdProject import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^base/$', views.base, name='base'),
    url(r'^ebooks/$', views.ebooks, name='ebooks'),
    url(r'^ebooks/(?P<category>.*)/$', views.ebooks, name='ebooks'),

    url(r'ebookdetail/(?P<pk>[0-9]+)/$', follow, name='ebook_custom_detail'),  # everybody
    url(r'ebookdetail/(?P<book_k>[0-9]+)/forum/(?P<forum_k>[0-9]+)/$', ebook_forum, name='forumdetail'),
    url('changebook/(?P<pk>[0-9]+)/$', views.change_ebook, name='Ebook_change_details'),
    # only staff (admin and support)

    url('User/$', UserList.as_view(), name='users'),  # remove
    url(r'^User/(?P<username>\w+)/$', UserDetail.as_view()),  # remove

    url('uploadFile/', upload_file, name='upload_file'),  # only logged in

    url('login/', login_create_view, name='login'),  # everybody
    url('signup/', signup_create_view, name='signup'),  # everybody

    url('provider/', provider_page, name='provider_page'),  # only self provider!!!!!
    url('contract/', contract_page, name='contract_page'),  # only self provider!!!!!
    url('addbook/', ebook_create_view, name='add_book'),  # only provider!!!!

    url('ticket/(?P<pk>[0-9]+)/$', ticketForumView, name='ticket_detail'),
    url('tickets/', support_page, name='support_page'),

    url(r'^profile/(?P<username>\w+)/$', user_profile_page.as_view(), name='userprofilepage'),  # only self
    url(r'^profile/(?P<username>\w+)/edit/$', edit_profile_page, name='edituserprofile'),  # only self
    url(r'^profile/(?P<username>\w+)/upgrade/$', upgrade_account_view, name='upgradeaccount'),  # only self
    url(r'^profile/(?P<username>\w+)/updatepayment/$', update_payment_details, name='updatepayment'),
    url(r'^profile/(?P<username>\w+)/cancelconfirmation/$', downgrade_account_view, name='cancelconfirmation'),

]

# url('ebooklist/', ebookListView.as_view(), name='ebook_custom_list'),

urlpatterns = format_suffix_patterns(urlpatterns)
# urlpatterns += staticfiles_urlpatterns()
urlpatterns += [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
