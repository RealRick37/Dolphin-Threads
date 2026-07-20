from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

User=get_user_model()

class RegisterAPITest(APITestCase):
    def test_user_can_register(self):
        url=reverse("api_register")

        data={
            "username": "kivy",
            "email": "kivy@test.com",
            "password": "kivy123456!",
            "password2": "kivy123456!"
        }

        response=self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)