"""
Custom user model and user manager for authentication.
This file defines a custom User model using email as the unique identifier,
and a UserManager to handle user and superuser creation.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Custom user manager to handle user creation with email and full_name
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, full_name, username=None, **extra_fields):
        """
        Internal method to create and save a user with the given email, full name, and password.
        Username is ignored for compatibility with AbstractUser.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, full_name=None, username=None, **extra_fields):
        """
        Create and save a regular user with the given email, full name, and password.
        """
        if full_name is None:
            raise TypeError('The full_name field is required.')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, full_name, username, **extra_fields)

    def create_superuser(self, email, password, full_name, username=None, **extra_fields):
        """
        Create and save a superuser with the given email, full name, and password.
        Ensures is_staff and is_superuser are set to True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, full_name, username, **extra_fields)

class User(AbstractUser):
    """
    Custom User model that uses email as the unique identifier instead of username.
    Includes a full_name field.
    """
    username = None  # Remove username field from AbstractUser
    email = models.EmailField(unique=True)  # Use email as unique identifier
    full_name = models.CharField(max_length=255)  # Store user's full name

    USERNAME_FIELD = "email"  # Set email as the USERNAME_FIELD for authentication
    REQUIRED_FIELDS = ["full_name"]  # full_name is required for createsuperuser

    objects = UserManager()  # Use the custom user manager

    def __str__(self):
        """
        String representation of the user, returns the email.
        """
        return self.email
