from django.apps import AppConfig
import sys
from django.contrib.auth import get_user_model

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        if 'migrate' in sys.argv or 'makemigrations' in sys.argv:
            return
        User=get_user_model()

        if not User.objects.filter(role='admin').exists():
            User.objects.create_superuser(
                username="kavitha3805",
                email="kavitharavichandran3805@gmail.com",
                password="kavitha",
                role="admin"
            )
