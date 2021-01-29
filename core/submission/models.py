from django.db import models
from users.models import User
from questions.models import Question


# Create your models here.

class Submission(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, verbose_name='user_id')
    language_type = models.IntegerField(default=1, blank=False, null=False, verbose_name='language_type')
    questions_id = models.ForeignKey(Question, on_delete=models.CASCADE, blank=False, null=False,
                                     verbose_name='questions_id')
    checked_status = models.BooleanField(default=False, blank=False, null=False, verbose_name='checked_status')
    repo_url = models.CharField(default='None', blank=False, null=False, verbose_name='repo_url',max_length=255)
