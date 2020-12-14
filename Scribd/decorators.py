from django.http import HttpResponse
from django.shortcuts import redirect


def authentificated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("index")

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = []
            if request.user.groups.exists():
                for g in request.user.groups.all():
                    group.append(g.name)
            if [i for i in group if i in allowed_roles]:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("error")

        return wrapper_func

    return decorator
