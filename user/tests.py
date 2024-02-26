from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# Get the custom user model
User = get_user_model()

class UserTests(APITestCase):
    def test_create_user(self):
        """
        Test to ensure a new user can be created and the API returns a valid response.
        """
        # Define the URL for creating a new user using the 'user-list' URL name
        url = reverse('user:user-list')
        # Data to be sent in the request to create a new user
        data = {'email': 'test@example.com', 'username': 'testuser', 'password': 'testpass123'}
        # Make a POST request to create a new user
        response = self.client.post(url, data, format='json')
        # Check if the user was created successfully with HTTP 201 status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify the response contains the email and username, but not the password
        self.assertTrue('email' in response.data)
        self.assertTrue('username' in response.data)
        self.assertFalse('password' in response.data)
        # Ensure the user now exists in the database
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_user_login(self):
        """
        Test to ensure that a user can log in with correct credentials and receive a token.
        """
        # Create a user first to test login functionality
        self.test_create_user()
        # Define the URL for token authentication
        url = reverse('api_token_auth')
        # Credentials for logging in
        data = {'username': 'test@example.com', 'password': 'testpass123'}
        # Make a POST request to log in
        response = self.client.post(url, data, format='json')
        # Verify successful login with HTTP 200 status code and token in response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_user_logout(self):
        """
        Test to ensure that a logged-in user can log out successfully.
        """
        # Log in the user first before testing logout
        self.test_create_user()
        login_url = reverse('api_token_auth')
        login_data = {'username': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(login_url, login_data, format='json')
        # Extract the token from login response
        token = response.data['token']
        # Set the token in Authorization header for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        # Define the URL for logging out
        logout_url = reverse('user:logout')
        # Make a GET request to log out
        response = self.client.get(logout_url)
        # Verify successful logout with HTTP 200 status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Clear any credentials set on the client
        self.client.credentials()
