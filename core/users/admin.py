from django.contrib import admin
from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()

admin.site.register(User)

app = apps.get_app_config('graphql_auth')

# Register your models here.
for model_name, model in app.models.items():
    admin.site.register(model)
