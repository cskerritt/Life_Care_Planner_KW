from django.conf import settings
from django.contrib.auth import login
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.utils.http import is_safe_url
from health_check.views import MainView
from .forms import LoginForm


def home(request):
    if request.user.is_authenticated:
        return render(
            request,
            "web/app_home.html",
            context={
                "active_tab": "dashboard",
                "page_title": _("Dashboard"),
            },
        )
    else:
        return render(request, "web/landing_page.html")


def simulate_error(request):
    raise Exception("This is a simulated error.")


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            remember_me = form.cleaned_data['remember_me']
            
            login(request, user)
            
            if not remember_me:
                request.session.set_expiry(0)
            
            next_url = request.GET.get('next')
            if next_url and is_safe_url(next_url, allowed_hosts=None):
                return redirect(next_url)
            return redirect('dashboard:index')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


class HealthCheck(MainView):
    def get(self, request, *args, **kwargs):
        tokens = settings.HEALTH_CHECK_TOKENS
        if tokens and request.GET.get("token") not in tokens:
            raise Http404
        return super().get(request, *args, **kwargs)
