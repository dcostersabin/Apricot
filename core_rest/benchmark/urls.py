from django.urls import path
import benchmark.views as v

urlpatterns = [
    path('', v.benchmark),
    path('<int:submission_id>', v.benchmark_submission)
]
