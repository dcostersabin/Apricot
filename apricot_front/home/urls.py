from django.urls import path
from home import views as v

urlpatterns = [
    path('', v.home, name='home'),
    path('oauth/verified/<str:refresh>/<str:token>', v.oauth),
    path('login', v.login, name='login'),
    path('dashboard', v.dash, name='dash'),
    path('logout', v.logout),
    path('refresh_repo', v.refresh_repo),
    path('login', v.login),
    path('submit/<str:id>/<str:username>/<str:reponame>', v.submit),
    path('benchmark/<str:submission_id>', v.benchmark),
    path('view_score/<str:submission_id>', v.view_score),
    path('add_question', v.add_question),
]
