from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(null=True , unique=True)
    registration_no = models.CharField(max_length=200 , unique=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=200 ,blank=True, null=True)

    def __str__(self):
       return self.username

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , blank=True, null=True)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    username = models.CharField(max_length = 30)
    email = models.EmailField(null=True , unique=True)
    registration_no = models.CharField(max_length=200 , unique=True)

    def __str__(self):
        return self.username