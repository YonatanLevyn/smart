from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson

class CourseViewSetTestCase(APITestCase):

    def setUp(self):
        ## Using get_user_model() instead of User.objects.create_user() to avoid hardcoding the User model
        ## This is useful when you have a custom user model
        ## Also if you change the user model in the future, you won't have to change the tests
        self.user = get_user_model().objects.create_user(email='testuser@test.com', username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        self.course = Course.objects.create(title="Test Course", description="Test Description", created_by=self.user)
        self.lesson = Lesson.objects.create(title="Python Basics", description="Learn variables and data types in Python", youtube_video_id= "YOUTUBE_ID", course=self.course)

        self.lesson_data = {
            "title": "Python Basics", 
            "description": "Learn variables and data types in Python", 
            "youtube_video_id": "YOUTUBE_ID", 
            "course": self.course.id
        }

    def api_authentication(self):
        ## Now we can use self.client.credentials() to authenticate the requests
        ## In each request, the token will be added to the Authorization header
        ## So we dont need to login in each test
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_course(self):
        data = {"title": "Python for beginners", "description": "Learn python programming from scratch"}
        response = self.client.post(reverse('course-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_course(self):
        response = self.client.get(reverse('course-detail', kwargs={'pk': self.course.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course(self):
        data = {"title": "Advanced Python", "description": "Master python programming"}
        response = self.client.put(reverse('course-detail', kwargs={'pk': self.course.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_course(self):
        response = self.client.delete(reverse('course-detail', kwargs={'pk': self.course.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

    def test_retrieve_lesson(self):
        response = self.client.get(reverse('lesson-detail', kwargs={'pk': self.lesson.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        response = self.client.put(reverse('lesson-detail', kwargs={'pk': self.lesson.pk}), self.lesson_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        response = self.client.delete(reverse('lesson-detail', kwargs={'pk': self.lesson.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

