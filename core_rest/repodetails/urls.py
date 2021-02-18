from django.urls import path
import repodetails.views as v

urlpatterns = [
    path('', v.refresh_repo)
]
