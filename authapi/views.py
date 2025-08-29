import secrets
import redis
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer

User = get_user_model()
r = redis.from_url(settings.CACHES["default"]["LOCATION"])

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "login"

    def post(self, request):
        s = RegisterSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response({"message": "registered"}, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    throttle_scope = "login"

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({"email": u.email, "full_name": u.full_name})

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "password_reset"

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "email required"}, status=400)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "if account exists, reset token generated"})
        token = secrets.token_urlsafe(32)
        r.setex(f"pwdreset:{token}", 600, str(user.id))
        return Response({"reset_token": token, "expires_in": 600})

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "password_reset"

    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        if not token or not new_password:
            return Response({"detail": "token and new_password required"}, status=400)
        user_id = r.get(f"pwdreset:{token}")
        if not user_id:
            return Response({"detail": "invalid or expired token"}, status=400)
        try:
            user = User.objects.get(id=int(user_id))
        except User.DoesNotExist:
            return Response({"detail": "invalid token"}, status=400)
        user.set_password(new_password)
        user.save()
        r.delete(f"pwdreset:{token}")
        return Response({"message": "password reset successful"})