from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from Scribd.views import lista_libros, base, add_books_form, ebookList, ebookDetail, ebook_create_view, ebookListView, ebookDetailView

# endpoints

urlpatterns = [
    url(r'^$', lista_libros, name='mainpage'),
    url(r'^base/$', base, name='base'),
    url('predef-ebooklist/$', ebookList.as_view(), name='ebook_list'),
    url('predef-ebookdetail/(?P<pk>[0-9]+)/$', ebookDetail.as_view(), name='ebook_detail'),
    url('ebooklist/$', ebookListView.as_view(), name='ebook_custom_list'),
    url('ebookdetail/(?P<pk>[0-9]+)/$', ebookDetailView.as_view(), name='ebook_custom_detail'),
    url('addbook/', ebook_create_view, name='add_book'),
]

urlpatterns = format_suffix_patterns(urlpatterns)