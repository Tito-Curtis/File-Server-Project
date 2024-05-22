from django import forms
from django.core.validators import RegexValidator
import re
import os

def password_validations(password):
            specialChar= "!@#$%^&*()-_=+[{]}:|;'<,>.?/\\`~"  
            password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\d])(?=.*['+re.escape(specialChar)+r'])[A-Za-z\d'+ re.escape(specialChar)+r']+$'
            if len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long")
            
            
            validator = RegexValidator(
            regex=password_pattern,
            message="Password must contain alphanumeric with at least 1 special character and an uppercase.",
            code="invalid_password")

            validator(password)
            return password
def document_file_validation(file):
        ext = os.path.splitext(file.name)[1]
        valid_extensions = '.pdf'
        if ext != valid_extensions:
            raise forms.ValidationError('Unsupported file extension, file format should be .pdf')
        