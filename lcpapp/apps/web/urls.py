from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views

app_name = "web"
urlpatterns = [
    path("", views.home, name="home"),
    path("terms/", TemplateView.as_view(template_name="web/terms.html"), name="terms"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots.txt"),
    # these views are just for testing error pages
    # actual error handling is handled by Django: https://docs.djangoproject.com/en/4.1/ref/views/#error-views
    path("400/", TemplateView.as_view(template_name="400.html"), name="400"),
    path("403/", TemplateView.as_view(template_name="403.html"), name="403"),
    path("404/", TemplateView.as_view(template_name="404.html"), name="404"),
    path("500/", TemplateView.as_view(template_name="500.html"), name="500"),
    path("simulate_error/", views.simulate_error),
    path("health/", views.HealthCheck.as_view(), name="health_check"),

    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='auth/password_reset.html',
        email_template_name='auth/password_reset_email.html',
        subject_template_name='auth/password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done')
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'
    ), name='password_reset_complete'),
]
