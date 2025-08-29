import secrets
import redis
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_redis import get_redis_connection
from drf_spectacular.utils import extend_schema, OpenApiExample
import uuid

from .serializers import (
    RegisterSerializer, LoginSerializer, ForgotPasswordSerializer,
    ResetPasswordSerializer, UserSerializer
)

User = get_user_model()
r = redis.from_url(settings.CACHES["default"]["LOCATION"])

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = "login"

    @extend_schema(
        request=RegisterSerializer,
        responses={201: UserSerializer},
        examples=[OpenApiExample(
            "Register Example",
            value={"email": "user@example.com", "full_name": "John Doe", "password": "strongpassword123"}
        )]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "login"

    @extend_schema(
        request=LoginSerializer,
        responses={200: OpenApiExample(
            "JWT Token Example",
            value={"access": "jwt-access-token", "refresh": "jwt-refresh-token"}
        )},
        examples=[OpenApiExample(
            "Login Example",
            value={"email": "user@example.com", "password": "strongpassword123"}
        )]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request, email=serializer.validated_data["email"], password=serializer.validated_data["password"]
        )
        if not user:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: UserSerializer},
        description="Get authenticated user details."
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "password_reset"

    @extend_schema(
        request=ForgotPasswordSerializer,
        responses={200: OpenApiExample(
            "Forgot Password Example",
            value={"detail": "Password reset email sent if user exists."}
        )}
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Password reset email sent if user exists."}, status=200)
        token = str(uuid.uuid4())
        redis_conn = get_redis_connection("default")
        redis_conn.set(f"reset:{token}", user.pk, ex=600)
        # Here you would send the token via email in production
        return Response({"detail": "Password reset email sent if user exists.", "reset_token": token})

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "password_reset"

    @extend_schema(
        request=ResetPasswordSerializer,
        responses={200: OpenApiExample(
            "Reset Password Example",
            value={"detail": "Password has been reset successfully."}
        )}
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]
        password = serializer.validated_data["password"]
        redis_conn = get_redis_connection("default")
        user_id = redis_conn.get(f"reset:{token}")
        if not user_id:
            return Response({"detail": "Invalid or expired token."}, status=400)
        try:
            user = User.objects.get(pk=int(user_id))
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)
        user.set_password(password)
        user.save()
        redis_conn.delete(f"reset:{token}")
        return Response({"detail": "Password has been reset successfully."})