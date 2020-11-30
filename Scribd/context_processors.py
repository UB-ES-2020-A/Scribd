from django.contrib.auth.forms import AuthenticationForm
from django import forms


def inject_login_form(request):
    return {'login_form': AuthenticationForm()}
