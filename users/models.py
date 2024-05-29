from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        # email = self.normalize_email(email)
        
        user = self.model(
            username = username,
            **extra_fields
        )
        
        user.set_password(password)
        
        user.save()
        
        return user
        
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username=username, password=password,**extra_fields)
    
class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=False, blank=True, null=True)
    username = models.CharField(max_length=45, unique=True)
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)

    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['username, first_name, last_name']
    
    def __str__(self) -> str:
        return self.username