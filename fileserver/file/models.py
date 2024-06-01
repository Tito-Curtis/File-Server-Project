from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from .validations import document_file_validation
from django.core.exceptions import ValidationError

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
         user.is_staff = True
         user.save(using=self._db)

         return user


class All_Users(AbstractBaseUser):
    firstName = models.CharField(max_length=50,null=False)
    lastName = models.CharField(max_length=50,null=False)
    email = models.EmailField(max_length=120,unique=True,null=False)
    password = models.CharField(max_length=300,null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['firstName','lastName']

    objects=UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    

class DocumentCategory(models.Model):
    category_name = models.CharField(max_length=100)
    def __str__(self):
        return self.category_name
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Document Categories'


class Document(models.Model):
    title          = models.CharField(max_length=100)
    description    = models.TextField()
    file           = models.FileField(upload_to='file/documents/',validators=[document_file_validation])
    uploaded_at    = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0)
    email_count    = models.PositiveIntegerField(default=0)
    category       = models.ForeignKey(DocumentCategory,on_delete=models.CASCADE)
    assigned_user  = models.ManyToManyField('All_Users', related_name='assigned_to_users')

    def increment_download_count(self):
        self.download_count += 1
        self.save()
    def increment_email_count(self):
        self.email_count += 1
        self.save()
    
   
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
          
class ContactAdmin(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey(All_Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Admin Messages'
    def __str__(self):
        return f'{self.user.firstName} {self.user.lastName}' 