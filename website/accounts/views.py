from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from verify_email.email_handler import send_verification_email

from .forms import CustomUserCreationForm, LoginForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # Override form_valid method to add custom logic after the form is validated
        response = super().form_valid(form)

        # Call your function to send verification email
        send_verification_email(self.request, form)

        return response


from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import FormView

class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        
        else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)
