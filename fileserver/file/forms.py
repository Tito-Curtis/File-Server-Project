from django import forms
from .models import All_Users
from django.core.validators import RegexValidator
import re


class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField()
    class Meta:
        model = All_Users
        fields = ['firstName', 'lastName','email', 'password','confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
            },
        labels = {
            'firstName': 'First Name',
            'lastName': 'Last Name',
            'email': 'Email',
            'password': 'Password',
            'confirm_password': 'Confirm Password',}
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if All_Users.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already used")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        specialChar= "!@#$%^&*()-_=+[{]}:|;'<,>.?/\\`~"  #p
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\d])(?=.*['+re.escape(specialChar)+r'])[A-Za-z\d'+ re.escape(specialChar)+r']+$'

        #password_pattern = r"[a-zA-Z0-9\s" + re.escape(specialCharacters) + r"]+"
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long")
        
        
        validator = RegexValidator(
        regex=password_pattern,
        message="Password must contain at least one special character, digit and both case letters",
        code="invalid_password")

        validator(password)
        
            
        return cleaned_data
    def save(self,commit=True):
        user = super().save(commit=False)
        user.password = self.cleaned_data.get('password')
        user.firstName = self.cleaned_data.get('firstName').lower()
        user.lastName = self.cleaned_data.get('lastName').lower()
        user.email    = self.cleaned_data.get('email').lower()

        if commit:
            user.save()
        return user
        


        