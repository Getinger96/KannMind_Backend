from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """
    Extended profile model for additional user information.

    This model creates a one-to-one relationship with Django's built-in User model
    and adds extra fields such as bio and location.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the user profile.

        Returns:
            str: The username of the associated User instance.
        """
        return self.user.username
