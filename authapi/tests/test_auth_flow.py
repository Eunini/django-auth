from django.urls import reverse
from rest_framework.test import APITestCase
from accounts.models import User
from rest_framework import status

class AuthFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", full_name="Test User", password="testpass123"
        )

    def test_register(self):
        url = reverse("register")
        data = {"email": "new@example.com", "full_name": "New User", "password": "newpass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", response.data)

    def test_login(self):
        url = reverse("login")
        data = {"email": "test@example.com", "password": "testpass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.access = response.data["access"]

    def test_me(self):
        self.test_login()
        url = reverse("me")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_forgot_password(self):
        url = reverse("forgot-password")
        data = {"email": "test@example.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("detail", response.data)
        self.assertIn("reset_token", response.data)

    def test_reset_password(self):
        # Get reset token
        url = reverse("forgot-password")
        data = {"email": "test@example.com"}
        response = self.client.post(url, data)
        token = response.data.get("reset_token")
        # Reset password
        url = reverse("reset-password")
        data = {"token": token, "password": "resetpass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("detail", response.data)
        # Login with new password
        url = reverse("login")
        data = {"email": "test@example.com", "password": "resetpass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
