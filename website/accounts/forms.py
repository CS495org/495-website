from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    # password1 = forms.PasswordInput(attrs={"placeholder" : "Enter Password"})
    # password2 = forms.PasswordInput(attrs={"placeholder" : "Confirm Password"})

    class Meta:
        model = CustomUser
        fields = ("username", "email") # , "password1", "password2")
        widgets = {
            "username" : forms.TextInput(attrs={"placeholder" : "Username"}),
            "email" : forms.EmailInput(attrs={"placeholder" : "Email"}),
            # "password1" : forms.PasswordInput(attrs={"placeholder" : "Enter Password"}),
            # "password2" : forms.PasswordInput(attrs={"placeholder" : "Confirm Password"}),
        }

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")