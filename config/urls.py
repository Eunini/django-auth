from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from authapi.views import RegisterView, LoginView, MeView, ForgotPasswordView, ResetPasswordView

def root(request):
    return JsonResponse({"message": "Welcome to the Auth Service API. See /api/docs/ for documentation."})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/register", RegisterView.as_view(), name='register'),
    path("api/auth/login", LoginView.as_view(), name='login'),
    path("api/auth/me", MeView.as_view(), name='me'),
    path("api/auth/forgot-password", ForgotPasswordView.as_view(), name='forgot-password'),
    path("api/auth/reset-password", ResetPasswordView.as_view(), name='reset-password'),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("", root),
]
