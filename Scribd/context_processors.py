from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import  redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from Scribd.forms import RegisterForm


def inject_login_form(request):
    return  {'login_form': AuthenticationForm()}
