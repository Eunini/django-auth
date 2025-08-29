from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()

class AuthFlowTests(APITestCase):
    def setUp(self):
        self.email = "test@example.com"
        self.password = "StrongPass123!"
        self.full_name = "Test User"

    def test_register_login_me(self):
        r = self.client.post("/api/auth/register", {
            "full_name": self.full_name, "email": self.email, "password": self.password
        })
        self.assertEqual(r.status_code, 201)

        r = self.client.post("/api/auth/login", {"email": self.email, "password": self.password})
        self.assertEqual(r.status_code, 200)
        access = r.data["access"]

        r = self.client.get("/api/auth/me", HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["email"], self.email)

    def test_forgot_and_reset(self):
        User.objects.create_user(email=self.email, full_name=self.full_name, password=self.password)
        r = self.client.post("/api/auth/forgot-password", {"email": self.email})
        self.assertEqual(r.status_code, 200)
        token = r.data["reset_token"]

        r = self.client.post("/api/auth/reset-password", {"token": token, "new_password": "NewPass123!"})
        self.assertEqual(r.status_code, 200)
