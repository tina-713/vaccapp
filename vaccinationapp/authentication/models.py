from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone



class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
      if email is None:
          raise TypeError('Please provide an email address')

      user = self.model(email=self.normalize_email(email))
      user.set_password(password)
      user.save()
      return user

    def create_superuser(self, email, password=None):
      if password is None:
          raise TypeError('Password should not be none')

      user = self.create_user(email, password)
      user.is_superuser = True
      user.is_user = True
      user.save()
      return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'email': 'email'}


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class UserActivationToken(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    datetime = models.DateField(default=timezone.now)  # for token expiration