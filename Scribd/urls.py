from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from Scribd.views import lista_libros, base, ebook_create_view, ebookListView, ebookDetailView, signup_create_view, \
    login_create_view #providers_homepage_view

# endpoints

urlpatterns = [
    url(r'^$', lista_libros, name='mainpage'),
    url(r'^base/$', base, name='base'),
    url('ebooklist/', ebookListView.as_view(), name='ebook_custom_list'),
    url('ebookdetail/(?P<pk>[0-9]+)/$', ebookDetailView.as_view(), name='ebook_custom_detail'),
    url('addbook/', ebook_create_view, name='add_book'),
    url('accounts/login/', login_create_view, name='login'),
    url('accounts/signup/', signup_create_view, name='signup'),
    #url('providers/', providers_homepage_view, name='providers_homepage'),
]

urlpatterns = format_suffix_patterns(urlpatterns)


