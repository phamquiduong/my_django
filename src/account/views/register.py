from http import HTTPMethod, HTTPStatus

from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from account.forms.register import RegisterForm


def register_view(request: HttpRequest) -> HttpResponse:
    form = RegisterForm(request.POST or None)

    if request.method == HTTPMethod.POST and form.is_valid():
        user = form.save()
        login(request=request, user=user)
        messages.success(request, "Create account successfully. Welcome to my website")
        return redirect("home")

    return render(request, "pages/register.html", {"form": form}, status=HTTPStatus.CREATED)
