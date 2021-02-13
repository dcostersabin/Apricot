from django.urls import path
from questions import views as v

urlpatterns = [

    path('add/', v.add)
]
