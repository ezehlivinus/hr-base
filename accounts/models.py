from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ('USER', 'User'),
        ('ORG_ADMIN', 'Organization Admin'),
        ('ORG_STAFF', 'Organization Staff'),
        ('ORG_HR', 'Organization HR')
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='USER')

    def __str__(self):
        return self.name
