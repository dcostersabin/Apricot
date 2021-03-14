from django.db import models
from users.models import User
from django.dispatch.dispatcher import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialToken
from users.models import User
import requests
from allauth.account.signals import email_confirmed
from questions.models import Question
from random import randint
from submission.models import Submission


class RepoDetail(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
                                verbose_name='user_id')
    repo_name = models.CharField(max_length=255, blank=False, null=False, verbose_name='repo_name')
    repo_full_name = models.CharField(max_length=255, blank=False, null=False, verbose_name='repo_full_name')
    private = models.BooleanField(default=False, null=False, verbose_name='private')
    owner_login = models.CharField(max_length=255, blank=False, null=False, verbose_name='owner_login')
    owner_avatar_url = models.CharField(max_length=255, blank=False, null=False, verbose_name='owner_avatar_url')
    html_url = models.CharField(max_length=255, blank=False, null=False, verbose_name='html_url')
    clone_url = models.CharField(max_length=255, blank=False, null=False, verbose_name='clone_url')
    size = models.CharField(max_length=255, blank=False, null=False, verbose_name='repo_size')
    language = models.CharField(max_length=255, blank=True, null=True, verbose_name='language')

    def serializer(self):
        data = {
            'user_id': self.user_id.id,
            'repo_name': self.repo_name,
            'repo_full_name': self.repo_full_name,
            'private': self.private,
            'owner_login': self.owner_login,
            'owner_avatar_login': self.owner_avatar_url,
            'html_url': self.html_url,
            'clone_url': self.clone_url,
            'size': self.size,
            'language': self.language
        }
        return data


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    social_user_token = SocialToken.objects.get(account__user=user)
    url = "https://api.github.com/search/repositories?q=user:" + user.username + "&per_page=200"
    r = requests.get(url, headers={'Authorization': 'token ' + social_user_token.token})
    data = r.json()
    for obj in data['items']:
        d = RepoDetail()
        d.user_id = User.objects.get(email=user.email)
        d.repo_name = obj['name']
        d.repo_full_name = obj['full_name']
        d.private = obj['private']
        d.owner_login = obj['owner']['login']
        d.owner_avatar_url = obj['owner']['avatar_url']
        d.html_url = obj['html_url']
        d.clone_url = obj['clone_url']
        d.size = obj['size']
        d.language = obj['language']
        d.save()


@receiver(email_confirmed)
def email_confirmed(request, email_address, **kwargs):
    user = User.objects.get(email=email_address)
    # get all questions stored
    question_count = Question.objects.all().count()
    if question_count > 0:
        index = randint(0, question_count - 1)
        question = Question.objects.all()
        # assigning random question to the user
        user_question = question[index]
        submission = Submission()
        submission.user_id = user
        submission.question_id = user_question
        submission.save()
