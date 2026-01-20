from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("researcher", "Researcher"),
        ("guest", "Guest"),
        ("auditor", "Auditor"),
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default="guest")
    phone = models.CharField(max_length=15, blank=True, null=True)
    limit = models.CharField(
        blank=True, null=True,
        max_length=15
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
