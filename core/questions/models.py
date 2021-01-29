from django.db import models


# Create your models here.

class Question(models.Model):
    details = models.TextField(blank=False, verbose_name='details')
    inputs = models.TextField(blank=False, verbose_name='inputs')
    output = models.TextField(blank=False, verbose_name='output')


