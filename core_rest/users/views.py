from rest_framework.decorators import api_view
from rest_framework.response import Response
from allauth.account.decorators import login_required
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.http.response import JsonResponse


@login_required(login_url='/root')
def token(request):
    refresh = RefreshToken.for_user(request.user)
    # since allauth initiates session based authentication
    # logging out from session based authentication after token is received from github
    logout(request)
    return JsonResponse({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


@api_view(['GET', 'POST'])
def bad_request(request):
    return Response("Not Authorized", status=HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def logout(request):
    if request.user.is_authenticated:
        return Response("User Is Still Logged In", HTTP_400_BAD_REQUEST)
    return Response("No User Logins")
