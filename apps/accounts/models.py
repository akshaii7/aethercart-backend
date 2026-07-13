from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("driver", "Driver"),
        ("admin", "Admin"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name