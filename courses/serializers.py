from rest_framework import serializers
from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer): 
    # with 'source='created_by.username' we can serialize a specific attribute of a related object
    # rather than the entire object (User in that case)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Course
        # Explicitly list all fields to be included in the serialized representation.
        # This provides control over the API output, ensuring only specified fields are included.
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 'updated_at']

class LessonSerializer(serializers.ModelSerializer):

    # SerializerMethodField is used here to include the title of the associated course without initiating new queries for each lesson.
    # nested serializer also could have worked but we need just a single piece of information from the object 
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
    

