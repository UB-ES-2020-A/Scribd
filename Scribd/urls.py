from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from Scribd import views
from Scribd.views import ebookList, ebookDetail, AccountList, AccountDetail
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

# endpoints
urlpatterns = [
    url(r'^$', views.lista_libros, name='mainpage'),
    url(r'^base/$', views.base, name='base'),
    url('ebook/$', ebookList.as_view()),
    url('ebook/(?P<pk>[0-9]+)/$', ebookDetail.as_view()),
    url('Account/$', AccountList.as_view()),
    url('Account/(?P<pk>[0-9]+)/$', AccountDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)