# users/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None):
        if not username:
            raise ValueError('Users must have a username')
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(username=username, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password):
        user = self.create_user(username, phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    USERNAME_FIELD = 'phone_number'  
    REQUIRED_FIELDS = ['phone_number','username']

    objects = UserManager()


