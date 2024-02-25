from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Course
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

class CourseAPITestCase(APITestCase):

    def setUp(self):

        # Get the custom User model
        User = get_user_model()

        # Create a user
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        
        # Obtain a token for the created user by making a POST request to the token endpoint
        response = self.client.post(reverse('api_token_auth'), {'username': 'testuser@example.com', 'password': 'testpassword'})
        self.token = response.data['token']
        
        # Add the obtained token to the Authorization header for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        
        # Create a course instance for testing
        self.course = Course.objects.create(title="Test Course", description="Test Description", created_by=self.user)


    def test_get_course_list(self):
        """
        Ensure we can retrieve the course list.
        """
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course(self):
        """
        Ensure we can create a new course object.
        """
        url = reverse('course-list')
        data = {'title': 'New Course', 'description': 'New Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_update_course(self):
        """
        Ensure we can update an existing course object.
        """
        url = reverse('course-detail', args=[self.course.id])
        updated_data = {'title': 'Updated Test Course', 'description': 'Updated Test Description'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Fetch the updated course from the database
        updated_course = Course.objects.get(id=self.course.id)
        self.assertEqual(updated_course.title, 'Updated Test Course')
        self.assertEqual(updated_course.description, 'Updated Test Description')

    def test_delete_course(self):
        """
        Ensure we can delete a course object.
        """
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the course no longer exists in the database
        exists = Course.objects.filter(id=self.course.id).exists()
        self.assertFalse(exists)
