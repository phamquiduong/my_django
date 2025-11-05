from http import HTTPMethod

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from account.decorators.login import require_login
from account.forms.profile import ProfileForm
from account.models import Province


@require_login
def profile_view(request: HttpRequest) -> HttpResponse:
    form = ProfileForm(request.POST or None, instance=request.user)

    if request.method == HTTPMethod.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Update profile success')
            return redirect('account_profile')
        messages.error(request, 'Update profile error. Please check your information')

    context = {
        'provinces': Province.objects.all(),
        'form': form,
    }
    return render(request, 'pages/profile.html', context)
