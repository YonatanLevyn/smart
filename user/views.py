from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import logout
from rest_framework import status
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token


class UserViewSet(ModelViewSet):
    """
    A viewset for viewing and editing user instances. This class is responsible for handling
    all requests related to users, such as creating a new user, retrieving user information,
    and updating user details. It utilizes Django REST Framework's conventions to simplify
    the creation of RESTful APIs.
    """
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Dynamically sets permission classes based on the action being performed. For creating
        a new user (sign up), it allows any request (AllowAny). For all other actions, it requires
        the user to be authenticated (IsAuthenticated). This ensures that unauthenticated users can
        only sign up and cannot access or modify any other user data.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        # The request is permitted only if it satisfies all listed permissions.
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Chooses the appropriate serializer based on the action. For the 'create' action, it uses
        UserRegisterSerializer to safely handle user registration, including password hashing.
        For all other actions, UserSerializer is used to manage user data serialization, which
        excludes sensitive information like passwords from the response.
        """
        if self.action == 'create':
            return UserRegisterSerializer
        else:
            return UserSerializer

    def create(self, request, *args, **kwargs):
        """
        Custom implementation of the create action to register a new user. It uses the appropriate
        serializer to validate and save the user data. After saving the user, it generates a token
        for immediate authentication, enhancing the registration flow by eliminating the need for
        a separate login request. This token is then included in the successful response, allowing
        the client to proceed with authenticated actions without additional steps.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # get_or_create prevents race conditions during object creation by ensuring that the check for an object's 
        # existence and its potential creation are executed as an atomic transaction
        token, created = Token.objects.get_or_create(user=user)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {'user': serializer.data, 'token': token.key},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class LogoutView(APIView):
    """
    Provides a logout mechanism for authenticated users.
    Simply calls Django's logout method and returns HTTP 200 OK status.
    """
    permission_classes = [IsAuthenticated]  

    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)

        

