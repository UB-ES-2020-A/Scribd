from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from Scribd.views import AccountList, AccountDetail

urlpatterns = [
    url('Account/$', AccountList.as_view()),
    url('Account/(?P<pk>[0-9]+)/$', AccountDetail.as_view())

]

urlpatterns = format_suffix_patterns(urlpatterns)