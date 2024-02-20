from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import logout
from rest_framework import status
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer
from rest_framework.viewsets import ModelViewSet


class UserViewSet(ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    - queryset retrieve all user instances.
    - get_permissions sets the permission_classes based on the action.
    - get_serializer_class selects the serializer class based on the action.
    """
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        # The request is permitted only if it satisfies all listed permissions.
        return [permission() for permission in permission_classes]


    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        else:
            return UserSerializer
    

class LogoutView(APIView):
    """
    Provides a logout mechanism for authenticated users.
    Simply calls Django's logout method and returns HTTP 200 OK status.
    """
    permission_classes = [IsAuthenticated]  

    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)

        

