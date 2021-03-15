from django.urls import path
from demo import views as v

urlpatterns = [
    path('reset', v.reset),
    path('assign', v.assign)
]
