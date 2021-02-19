from rest_framework.decorators import api_view
from rest_framework.response import Response
from repodetails.models import RepoDetail
from allauth.socialaccount.models import SocialToken
import requests
from rest_framework.status import HTTP_400_BAD_REQUEST


@api_view(['POST', 'GET'])
def refresh_repo(request):
    if request.method == 'POST':
        # get all the previous records
        if not request.user.is_staff and not request.user.is_superuser:
            user = request.user
            # delete all the previous records
            repo_details_prev = RepoDetail.objects.filter(user_id=user).delete()
            social_user_token = SocialToken.objects.get(account__user=user)
            url = "https://api.github.com/search/repositories?q=user:" + user.username
            r = requests.get(url, headers={'Authorization': 'token ' + social_user_token.token})
            data = r.json()
            for obj in data['items']:
                d = RepoDetail()
                d.user_id = user
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
            repo_details_prev = RepoDetail.objects.filter(user_id=user)
            data = [repo.serializer() for repo in repo_details_prev]
            return Response(data)
        else:
            return Response("Invalid Account Type", status=HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        if not request.user.is_staff and request.user.is_superuser:
            user = request.user
            repo_details = RepoDetail.objects.filter(user_id=user)
            data = [repo.serializer() for repo in repo_details]
            return Response(data)
        else:
            return Response("Invalid Account Type", status=HTTP_400_BAD_REQUEST)
