from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, CustomSetPasswordsForm,CustomPasswordResetForm
from django.contrib.auth import authenticate, login, logout
from .models import All_Users
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters


# Create your views here.
INTERNAL_RESET_SESSION_TOKEN =  "_password_reset_token"

User = get_user_model()
def index(request):
    return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'signup.html',{'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html',{'form':form})
def logout_view(request):
    logout(request)
    return redirect('index')

def error_404_view(request,exception=None):
    return render(request, '404.html',status=404)

def error_500_view(request,exception=None):
    return render(request, '500.html',status=500)

class CustomPasswordResetView(PasswordResetView):
    form_class= CustomPasswordResetForm
    template_name='reset_password.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordsForm
    template_name='reset_password_confirm.html'