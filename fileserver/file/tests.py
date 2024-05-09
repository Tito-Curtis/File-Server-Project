from django.test import TestCase
from django.urls import reverse
from .models import All_Users
from .forms import SignupForm,LoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


# Create your tests here.p :
class UserTestCase(TestCase):
    def setUp(self):
        
        self.data = {
            'firstName':'test',
            'lastName':'all',
            'email':'test@example.com',
            'password':'123A4r56<7'
        }
        get_user_model().objects.create_user(**self.data)     
            
        
    def test_user_creation(self):
        User = get_user_model()
        user = User.objects.create(
               firstName='test',lastName='all',email='test@gmail.com',password='1234'
        )
        self.assertEqual(user.firstName,'test')
        self.assertEqual(user.lastName,'all')
        self.assertEqual(user.email,'test@gmail.com')
        self.assertTrue(user.is_active)
    def test_user_signup(self):
        form_data = {
            'firstName': 'test',
            'lastName': 'all',
            'email': 'test@gmail.com',
            'password': '123A4r56<7',
            'confirm_password': '123A4r56<7'  
        }
        form = SignupForm(data=form_data)
        
        self.assertTrue(form.is_valid())
    
    def test_user_login(self):
        user = authenticate(email=self.data['email'], password=self.data['password'])
        self.assertTrue(user.is_active)
        
        
