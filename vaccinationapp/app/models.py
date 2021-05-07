from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.core.validators import MinLengthValidator, MinValueValidator
from vaccinationapp import settings

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
      if email is None:
          raise TypeError('Provide an email address')

      user = self.model(email=self.normalize_email(email))
      user.set_password(password)
      user.save()
      return user

    def create_superuser(self, email, password=None):
      if password is None:
          raise TypeError('Password should not be none')

      user = self.create_user(email, password)
      user.is_superuser = True
      user.is_staff = True
      user.save()
      return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'email': 'email'}



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.id)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }



class UserActivationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=250)
    datetime = models.DateField(default=timezone.now)  # for token expiration

    def __str__(self):
        return str(self.token)

    def getUser(self):
        UserActivationToken = self 
        user = UserActivationToken.user
        return str(user)

    def create_token(self, token, datetime,user):
        UserActivationToken = self
        UserActivationToken.token = token
        UserActivationToken.datetime = datetime
        UserActivationToken.user = User.objects.get(id=user)
        UserActivationToken.save()



class County(models.Model):
    name = models.CharField(max_length=30,blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)



class City(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=60,blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)



class Vaccine(models.Model):
    name = models.CharField(max_length=30,blank=False, null=False)
    booster_days = models.PositiveIntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)



class Categories(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=1000, blank=False)
    risk_count = models.PositiveIntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)



class Office(models.Model):
    name = models.CharField(max_length=500, blank=False)
    addres = models.CharField(max_length=500, blank=False)
    phone =models.CharField('phone', max_length=10, validators=[MinLengthValidator(10)])
    spots = models.PositiveIntegerField(default=0)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='office')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name='office')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)



class Person(models.Model):

    GENDER = (
        ('M', 'Masculin'),
        ('F', 'Feminin'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, blank=False, null=False) 
    last_name = models.CharField(max_length=60, blank=False, null=False)
    cnp =models.CharField('cnp', max_length=13, unique=True, validators=[MinLengthValidator(13)])
    gender = models.CharField(max_length=1, choices=GENDER)
    age = models.IntegerField(validators=[MinValueValidator(18)])
    phone =models.CharField('phone', max_length=10, validators=[MinLengthValidator(10)])
    email = models.EmailField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return str(self.name)
        