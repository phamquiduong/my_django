from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect


def require_login(view_func):
    def wrapped_view(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You need login.")
            return redirect("auth_login")
        return view_func(request, *args, **kwargs)

    return wrapped_view


def require_not_login(view_func):
    def wrapped_view(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return wrapped_view
