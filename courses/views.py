from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsOwnerOrReadOnly


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # Custom permissions to only allow owners of an object to edit it
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # created_by field is read-only in the serializer, it would not be set from the request data
        # so we explicitly sets the created_by field to the current user before saving the new course
        serializer.save(created_by=self.request.user)


class LessonViewSet(ModelViewSet):
    # 'select_related' performing a SQL join and includes the fields of the related object
    # because we know we will need to access the related objects of each instance in our queryset.
    queryset = Lesson.objects.select_related('course').all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
