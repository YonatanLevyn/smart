"""
models.py

This file contains the models for the user app.
At the moment, there is only one model, the User model,
which is a custom user model that extends the AbstractBaseUser
model provided by Django. This model is used to store user data
such as email, username, password, etc.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class UserManager(BaseUserManager):
    """
    Managers in Django are a way to interface with the database. 
    Django automatically creates one for every model named objects by default. 
    UserManager is extending Django's BaseUserManager and adding two additional methods: 
    create_user and create_superuser
    """
    def create_user(self, email, username=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('Invalid email address')
        
        if not username:
            username = email.split('@')[0]

        if password is not None:
            try:
                validate_password(password)
            except ValidationError as e:
                raise ValueError(', '.join(e.messages))
        else:
            raise ValueError('Password cannot be null')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        
        # handles the process of hashing the password and storing it securely
        """This approach differs from directly using Django's create method by 
            providing a secure way to handle password storage"""
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None):
        user = self.create_user(email,username=username,password=password)

        # The is_superuser flag grants the user all permissions automatically, bypassing all permission checks
        # for example, a superuser can view all objects in the database and edit them
        user.is_superuser = True

        # Save the changes to the superuser
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    """
    The AbstractBaseUser class provides core implementation of a User class, 
    including hashed passwords and tokenized password resets,
    there is no need to define password field in the User model.
    """
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30)
    publisher = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # telling Django to use our custom UserManager
    objects = UserManager()

    # These are attributes of the AbstractBaseUser class to handle user authentication
    # USERNAME_FIELD is the field that is used as the unique identifier
    # REQUIRED_FIELDS is a list of fields that are required when creating a superuser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
