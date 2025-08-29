"""
Admin configuration for the custom User model.
This file customizes how the User model appears and is managed in the Django admin interface.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for the User model.
    Configures the fields displayed and editable in the Django admin for users.
    """
    # Fields to display when viewing or editing a user
    fieldsets = (
        (None, {"fields": ("email", "password", "full_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "full_name", "password1", "password2")}),
    )
    # Columns to display in the user list view
    list_display = ("email", "full_name", "is_staff", "is_active")
    # Fields to enable search by in the admin
    search_fields = ("email", "full_name")
    # Default ordering for the user list
    ordering = ("email",)
