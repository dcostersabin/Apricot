from django.db import models


class Question(models.Model):
    details = models.TextField(blank=False, verbose_name='details', null=False)
    inputs = models.TextField(blank=False, verbose_name='inputs', null=False)
    output = models.TextField(blank=False, verbose_name='output', null=False)
