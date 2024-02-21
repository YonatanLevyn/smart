from rest_framework import serializers
from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer): 
    # Use ReadOnlyField to display the username of the user who created the course.
    # This ensures the field is read-only and not subject to modification via the API.
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Course
        # Explicitly list all fields to be included in the serialized representation.
        # This provides control over the API output, ensuring only specified fields are included.
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 'updated_at']

class LessonSerializer(serializers.ModelSerializer):

    # SerializerMethodField is used here to include the title of the associated course
    # without initiating new queries for each lesson, assuming the course data is prefetched.
    # it is used here insted of nested serializer because
    # we need just a single piece of information from the related object 
    course_title = serializers.SerializerMethodField()

    def get_course_title(self, obj):
        # This method retrieves the title of the course associated with this lesson.
        # It follows the pattern get_<field_name> expected by SerializerMethodField.
        return obj.course.title

    class Meta:
        model = Lesson
        # Includes the custom 'course_title' field along with the model's own fields.
        # This enhances the lesson's serialized data with contextual course information.
        fields = ['id', 'title', 'description', 'youtube_video_id', 'course', 'course_title', 'created_at', 'updated_at']
    

