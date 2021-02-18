from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.models import EmailAddress


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, verbose_name='email', max_length=255, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def serialized(self):
        email_verified = EmailAddress.objects.get(email=self.email)
        verified = email_verified.verified
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'last_login': self.last_login,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'joined_data': self.date_joined,
            'is_superuser': self.is_superuser,
            'verified': verified

        }
        return data


