from http import HTTPMethod

from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from account.forms.login import LoginForm


def login_view(request: HttpRequest) -> HttpResponse:
    form = LoginForm(request.POST or None)

    if request.method == HTTPMethod.POST and form.is_valid():
        login(request=request, user=form.user)
        messages.success(request, 'Welcome to my Website')
        return redirect('home')
    return render(request, 'pages/login.html', {'form': form})
