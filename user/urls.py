from django.urls import path, include
from .views import UserViewSet, LogoutView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('logout/', LogoutView.as_view(), name='logout'),
] 
