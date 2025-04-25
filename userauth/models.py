from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
# Create your models here.

#Custom User Model Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
# Custom User Model
class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100,null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email" #fields that can help log in
    REQUIRED_FIELDS = ['username'] #fields needed when creating superuser

    def __str__(self):
        return self.email

    @property
    def getvendor(self):
        try:
            return self.vendor  # Ensure this returns the Vendor object
        except:
            return None


