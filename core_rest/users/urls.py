from django.urls import path
import users.views as v

urlpatterns = [
    path('', v.user_info),
    path('<int:user_id>', v.user_info_admin)
]
