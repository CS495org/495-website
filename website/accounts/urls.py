from django.urls import path
from django.urls.base import reverse_lazy

from .views import SignUpView, LoginView

from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("password-change/", 
         PasswordChangeView.as_view(template_name="registration/password_change_form.html",
                                    success_url = reverse_lazy("password_change_done")), 
         name="password_change"),

    path("password-change-done/", 
         PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"), 
         name="password_change_done"),

    path('password-reset/', 
         PasswordResetView.as_view(template_name='registration/password_reset_form.html'), 
         name='password_reset'),

    path('password-reset/done/', 
         PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', 
         PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),

    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),
]