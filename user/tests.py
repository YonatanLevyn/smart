from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserRegisterViewTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@test.com', username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_registration(self):
        data = {
            "email": "user@test.com",
            "username": "testuser",
            "introduction": "Test Introduction",
            "password": "testpassword"
        }
        response = self.client.post(reverse('user:user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
