from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from authapi.views import RegisterView, LoginView, MeView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/register", RegisterView.as_view()),
    path("api/auth/login", LoginView.as_view(), name="token_obtain_pair"),
    path("api/auth/me", MeView.as_view()),
    path("api/auth/forgot-password", ForgotPasswordView.as_view()),
    path("api/auth/reset-password", ResetPasswordView.as_view()),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
