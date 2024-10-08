from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser, PermissionsMixin):
    ROLES = (
        ('USER', 'User'),
        ('ORG_ADMIN', 'Organization Admin'),
        ('ORG_STAFF', 'Organization Staff'),
        ('ORG_HR', 'Organization HR')
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='USER')

    is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)

    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # You can add more fields here if needed

    def __str__(self):
        return self.email

# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
#
# class User(AbstractUser):
#     ROLES = (
#         ('USER', 'User'),
#         ('ORG_ADMIN', 'Organization Admin'),
#         ('ORG_STAFF', 'Organization Staff'),
#         ('ORG_HR', 'Organization HR'),
#     )
#     role = models.CharField(max_length=20, choices=ROLES, default='USER')
#
#     def __str__(self):
#         return self.username
