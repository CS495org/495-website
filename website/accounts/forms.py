from django.contrib.auth.forms import (UserCreationForm,
                                       UserChangeForm,
                                       AuthenticationForm,
                                       UsernameField)
from django.utils.translation import gettext_lazy as gl
from .models import CustomUser
from django import forms
from django.views.generic.edit import UpdateView, FormView



class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=gl("Password"),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            }),
    )

    password2 = forms.CharField(
        label=gl("Password Confirmation"),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password Confirmation',
            }),
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email",)
        widgets = {
            "username" : forms.TextInput(attrs={"placeholder" : "Username"}),
            "email" : forms.EmailInput(attrs={"placeholder" : "Email"}),
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email",)



class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'
    }))