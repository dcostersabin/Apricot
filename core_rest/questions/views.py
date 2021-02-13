from rest_framework.decorators import api_view
from rest_framework.response import Response
from allauth.account.decorators import login_required
from rest_framework import status

# __LOGIN_URL__ = '/accounts/github/login/?process=login'


@api_view(['GET'])
@login_required
def add(request):
    if request.user.is_staff:
        user = request.user
        return Response(user.email)
    content = {'Permission Denied': 'You are not allowed to perform this'}
    return Response(content, status=status.HTTP_400_BAD_REQUEST)
