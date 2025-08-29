from rest_framework import serializers
from accounts.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ("id", "email", "full_name", "password")
        extra_kwargs = {"id": {"read_only": True}}
        example = {
            "email": "user@example.com",
            "full_name": "John Doe",
            "password": "strongpassword123"
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            full_name=validated_data["full_name"],
            password=validated_data["password"]
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    class Meta:
        example = {
            "email": "user@example.com",
            "password": "strongpassword123"
        }

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        example = {
            "email": "user@example.com"
        }

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        example = {
            "token": "reset-token-from-email",
            "password": "newstrongpassword123"
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "full_name")
        example = {
            "id": 1,
            "email": "user@example.com",
            "full_name": "John Doe"
        }
