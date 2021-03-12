from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    class Meta:
        db_table = 'm_users'

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=64)
    username = models.CharField(
        max_length=64,
        unique=False,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
