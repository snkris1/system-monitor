from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email Address")
    username = models.CharField(max_length=150, unique=True, verbose_name="Username")

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"