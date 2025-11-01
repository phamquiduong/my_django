from http import HTTPMethod

from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from account.forms.change_password import ChangePasswordForm


def change_password_view(request: HttpRequest) -> HttpResponse:
    form = ChangePasswordForm(request.POST or None, user=request.user)

    if request.method == HTTPMethod.POST and form.is_valid():
        user = form.save()
        login(request=request, user=user)
        messages.success(request, "Change password successfully.")
        return redirect("home")

    return render(request, "pages/change-password.html", {"form": form})
