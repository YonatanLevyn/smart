"""
Serializers in Django Rest Framework (DRF) are essentially bridges between 
complex data types such as Django models and Python data types that can then 
be easily rendered into JSON or XML or other content types 
which is suitable for client-side consumption.
"""
from rest_framework import serializers
from .models import User
from django.core.mail import send_mail
from django.conf import settings
import threading

# This serializer is used when you want to represent User instances. 
class UserSerializer(serializers.ModelSerializer):
    # Meta class automatically generates fields and validators based on the model
    class Meta:
        # Linking the serializer to my model 'User'
        model = User
        # Specifing which fields to include, this gives you control over what data is exposed via the API
        fields = ['email', 'username', 'publisher', 'is_active']
        read_only_fields = ['email', 'is_active']



# the deserialization process of creating new users, ensuring sensitive data like passwords are handled securely and not included in serialized output.
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}


    # Overriding the create method to use UserManager's create_user method
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        # Send welcome email after successful user creation
        send_welcome_email(user)
        return user


def send_welcome_email(user):
    subject = 'Welcome to Our Platform'
    message = f'Hi {user.username}, thank you for registering in our platform.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email,]
    
    # Define the email sending logic as a separate function
    def send_email():
        send_mail(subject, message, email_from, recipient_list)

    # Create and start a thread to send the email
    email_thread = threading.Thread(target=send_email)
    email_thread.start()