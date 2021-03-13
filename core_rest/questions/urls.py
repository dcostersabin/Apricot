from django.urls import path
from questions import views as v

urlpatterns = [
    path('', v.question),
    path('<int:question_id>/', v.question_one),
]
