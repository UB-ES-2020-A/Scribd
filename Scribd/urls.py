from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from Scribd.views import ebookList, ebookDetail

# endpoints
urlpatterns = [
    url('ebook/$', ebookList.as_view()),
    url('ebook/(?P<pk>[0-9]+)/$', ebookDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)