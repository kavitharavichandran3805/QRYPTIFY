"""
Enhanced signals for the home app with more features.
"""

from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
import logging
import os

logger = logging.getLogger(__name__)

@receiver(post_migrate)
def setup_initial_data(sender, **kwargs):
    if sender.name == 'home':
        create_admin_user()
        create_default_settings()

def create_admin_user():
    User = get_user_model()
    
    try:
        admin_username = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin')
        admin_email = os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'admin123')
        
        if not User.objects.filter(username=admin_username).exists():
            logger.info(f"Creating admin user: {admin_username}")

            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            logger.info(f"Admin user '{admin_username}' created successfully.")
        else:
            logger.info(f"Admin user '{admin_username}' already exists.")
            
    except Exception as e:
        logger.error(f"Failed to create admin user: {e}")

def create_default_settings():
    pass

@receiver(post_save, sender=get_user_model())
def log_user_creation(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New user created: {instance.username} ({instance.email})")