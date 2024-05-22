from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import (SignupForm, LoginForm, CustomSetPasswordsForm,
                    CustomPasswordResetForm,SendEmailForm)
from django.contrib.auth import authenticate, login, logout
from .models import All_Users,Document,DocumentCategory
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
import os

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


def feed_page_view(request):
    if request.user.is_authenticated:
        user = request.user
        documents = Document.objects.filter(assigned_user = user)
        return render(request, 'feed_page.html', {'documents': documents})
    else:
        return render(request, 'feed_page.html')

def download_document_view(request,document_id):
    document = get_object_or_404(Document, pk=document_id)
    document.increment_download_count()  
    return redirect(document.file.url)

def send_email_view(request,document_id):
    document_name = request.GET.get('document_name','')
    if request.method == 'POST':
        form = SendEmailForm(request.POST,request.FILES)
        document = Document.objects.get(id=document_id)  

        if form.is_valid():
            user_email = request.user.email 
            print(user_email)
            subject = form.cleaned_data['subject']
            recipient_email = form.cleaned_data['recipient_email']
            message = form.cleaned_data['message']
            file_name = os.path.basename(document.file.name)
            
            email =  EmailMessage(subject,message,from_email=user_email,to=[recipient_email])
            email.attach(file_name,document.file.read())
            try:
                email.send()
                document.increment_email_count()
                return HttpResponse('email sent successfully')
            except:
                return render(request,'500.html')
    else:
        form = SendEmailForm()
        context={
            'form': form,
            'document_name':document_name
        }
        return render(request,'send_email.html',context)
    
def view_documents(request,document_id):
    document = Document.objects.get(id=document_id)
    with open(document.file.path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename={}'.format(os.path.basename(document.file.name))
        return response

    