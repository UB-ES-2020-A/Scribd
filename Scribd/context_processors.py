from django.contrib.auth.forms import AuthenticationForm


def inject_login_form(request):
    return {'login_form': AuthenticationForm()}
