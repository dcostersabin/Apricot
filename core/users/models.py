from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, verbose_name='email', max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
