from django import forms
from .models import All_Users
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth.password_validation import validate_password
from .validations import password_validations



class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget= forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = All_Users
        fields = ['firstName', 'lastName','email', 'password','confirm_password']
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            
        }
        labels = {
            'firstName': 'First Name',
            'lastName': 'Last Name',
            'email': 'Email',
            'password': 'Password',
            'confirm_password': 'Confirm Password'}
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if All_Users.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already used")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        password_validations(password)        
        return cleaned_data
    def save(self,commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data.get('password'))
        user.firstName = self.cleaned_data.get('firstName').lower()
        user.lastName = self.cleaned_data.get('lastName').lower()
        user.email    = self.cleaned_data.get('email').lower()

        if commit:
            user.save()
        return user
class LoginForm(forms.Form):
    email = forms.EmailField(label='email',max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'you@example.com'}))
    password = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'password'}))

class CustomSetPasswordsForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New password',widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter a new password'}))
    new_password2 = forms.CharField(label='Confirm New password',widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm your new password '})) 

    error_message = {
        'password_mismatch': "Passwords do not match."
    }
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_message['password_mismatch'],
                    code='password_mismatch',
                )
        password_validations(password1)
        validate_password(password1, self.user)
        return password1
        
class CustomPasswordResetForm(PasswordResetForm):
     email = forms.EmailField(label='email',max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    
class SendEmailForm(forms.Form):
    subject = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    recipient_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))