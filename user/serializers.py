"""
Serializers in Django Rest Framework (DRF) are essentially bridges between 
complex data types such as Django models and Python data types that can then 
be easily rendered into JSON or XML or other content types 
which is suitable for client-side consumption.
"""
from rest_framework import serializers
from .models import User

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
        return user

