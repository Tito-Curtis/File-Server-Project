from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
     def create_user(self,firstName,lastName,email,password=None):
         if not email:
             raise ValueError('Users must have an email address')
         if not firstName:
             raise ValueError('Users must have a first name')
         if not lastName:
             raise ValueError('Users must have a last name')
         user = self.model(
             firstName=firstName,
             lastName=lastName,
             email=self.normalize_email(email),
         )
         user.set_password(password)
         user.save(using=self._db)
         return user
     def create_superuser(self,firstName,lastName,email,password=None):
         user= self.create_user(firstName=firstName,lastName=lastName,email=email,password=password)
         user.is_superuser = True
         user.is_admin = True
         user.staff = True
         user.save(using=self._db)

         return user


class All_Users(AbstractBaseUser):
    firstName = models.CharField(max_length=50,null=False)
    lastName = models.CharField(max_length=50,null=False)
    email = models.EmailField(max_length=120,unique=True,null=False)
    password = models.CharField(max_length=50,null=False)
    date_created = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['firstName','lastName']

    objects='UserManager'

    class Meta:
        verbose_name_plural = 'All Users'

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    
