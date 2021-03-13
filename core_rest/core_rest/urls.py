"""core_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import users.views as userview
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
import repodetails.urls as details
import users.urls as user
import questions.urls as questions
import submission.urls as submission
import benchmark.urls as benchmark

urlpatterns = [
    path('root/', userview.bad_request, name='root'),
    path('admin/', admin.site.urls),
    path('oauth/', include('allauth.urls')),
    path('token/', userview.token),
    path('frontend/', userview.frontend),
    path('log-out/', userview.logout),
    path('auth/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('repo/', include(details)),
    path('user/', include(user)),
    path('questions/', include(questions)),
    path('submission/', include(submission)),
    path('benchmarks/', include(benchmark)),
    path('log-out/frontend', userview.frontend_logout,)

]
