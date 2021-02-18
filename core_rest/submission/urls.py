from django.urls import path
import submission.views as v

urlpatterns = [
    path('', v.submission),
    path('<int:submission_id>', v.submission_one)
]
