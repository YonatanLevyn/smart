from django.db import models
from django.conf import settings
from django.urls import reverse

class Course(models.Model):
    """
    Represents a course that contains multiple lessons.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # with 'settings.AUTH_USER_MODEL' Django knows to use our custom user
    # related_name allows you to access a user's courses easily from the user instance (e.g., user.created_courses.all())
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_courses') 
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # Returns the URL to access a detail record for this course
        return reverse('courses:course_detail', args=[str(self.id)])


class Lesson(models.Model):
    """
    Represents a lesson belonging to a course.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    youtube_video_id = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:lesson_detail', args=[str(self.pk)])
