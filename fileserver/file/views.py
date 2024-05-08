from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import All_Users

# Create your views here.
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