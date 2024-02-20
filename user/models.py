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
        if not username:
            # set the username to the first part of the email address if no username is provided
            username = email.split('@')[0]

        # create a new instance of the user model
        # self.model automatically works with whichever model it's called on
        user = self.model(
            ## normalize_email() method to convert the email to all lowercase
            email = self.normalize_email(email),
            username = self.model.normalize_username(username)
        )

        # handles the process of hashing the password and storing it securely
        """This approach differs from directly using Django's create method by 
            providing a secure way to handle password storage"""
        user.set_password(password)

        # save() method to save the user object to the database
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username=None, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        # superuser is a user who has all permissions enabled
        # for example, a superuser can view all objects in the database and edit them
        user.is_superuser = True
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

    # Does the user have a specific permission? (Yes, if superuser)
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    # Does this user have permission to view this app? (ALWAYS YES FOR THE MOMENT)
    def has_module_perms(self, app_label):
        return True
    
    @staticmethod
    def normalize_username(username):
        "Normalize the username by making it lowercase"
        return username.lower()
