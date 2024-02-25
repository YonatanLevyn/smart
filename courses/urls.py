from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet

"""
    The DefaultRouter automatically generates URL patterns for a given viewset, 
    covering standard CRUD (Create, Read, Update, Delete) operations. 
    It uses the information provided by the viewset (such as the queryset 
    and serializer_class) to determine which actions are available and creates 
    the appropriate URLs for those actions.
"""

router = DefaultRouter()
router.register(r'', CourseViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
