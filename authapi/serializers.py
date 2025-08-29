"""
Serializers for authentication endpoints.
These handle validation and transformation of input/output data for registration, login, password reset, and user info.
"""

from rest_framework import serializers
from accounts.models import User

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates and creates a new user with email, full name, and password.
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "email", "full_name", "password")
        extra_kwargs = {"id": {"read_only": True}}
        # Example for OpenAPI/Swagger documentation
        example = {
            "email": "user@example.com",
            "full_name": "John Doe",
            "password": "strongpassword123"
        }

    def create(self, validated_data):
        """
        Create a new user instance with the provided validated data.
        """
        user = User.objects.create_user(
            email=validated_data["email"],
            full_name=validated_data["full_name"],
            password=validated_data["password"]
        )
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Validates email and password input.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        # Example for OpenAPI/Swagger documentation
        example = {
            "email": "user@example.com",
            "password": "strongpassword123"
        }

class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for forgot password endpoint.
    Validates the email input for password reset requests.
    """
    email = serializers.EmailField()

    class Meta:
        # Example for OpenAPI/Swagger documentation
        example = {
            "email": "user@example.com"
        }

class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for resetting the user's password.
    Validates the reset token and new password.
    """
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        # Example for OpenAPI/Swagger documentation
        example = {
            "token": "reset-token-from-email",
            "password": "newstrongpassword123"
        }

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for returning user details.
    Used for authenticated user info endpoints.
    """
    class Meta:
        model = User
        fields = ("id", "email", "full_name")
        # Example for OpenAPI/Swagger documentation
        example = {
            "id": 1,
            "email": "user@example.com",
            "full_name": "John Doe"
        }
