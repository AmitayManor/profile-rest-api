from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    """ Manager for user profiles """
    def create_user(self, email, name, password=None ):
        """ Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email) # some of the email providers are case sensetive, this func solve it
        user = self.model(email=email, name=name) # create a model of a user

        user.set_password(password) # Store the user's password as Encrypted Hash and not a plain String, this func solve it
        user.save(using=self._db) # Best practice convention to store data in multiple DBs in Django

        return user

    def create_superuser(self, email, name, password):
        """ Create a new super user profile """
        user= self.create_user(email, name, password)

        user.is_superuser=True
        user.is_staff = True
        user.save(using=self._db)

        return user



class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Database model for users in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email' # Overwrite that users defined by emails (by default its a REQUIRED_FIELD)
    REQUIRED_FIELDS = ['name'] # make 'name' a requirement for the users

    def get_full_name(self):
        """ Retrieve User's Full Name """
        return self.name

    def get_short_name(self):
        """ Retrieve User's Short Name (for right now it will return the same as 'get_full_name' """
        return self.name

    def __str__(self):
        """ Return String representation of the User's email """
        return self.email



