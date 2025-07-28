from rest_framework import serializers
from auth_app.models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.

    Serializes the user's additional profile information such as bio and location,
    and includes a reference to the associated User instance.
    """
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Accepts fullname, email, password, and repeated password.
    Validates email uniqueness and password match.
    Splits fullname into first and last name, creates a new User instance, 
    and sets the password securely.
    """

    fullname = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        """
        Validate that the email address is unique.

        Args:
            value (str): The email address provided by the user.

        Returns:
            str: The validated email address.

        Raises:
            serializers.ValidationError: If the email already exists.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate(self, data):
        """
        Validate that the password and repeated password match.

        Args:
            data (dict): The input data.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the passwords do not match.
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'error': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        """
        Create a new User instance based on the validated data.

        Args:
            validated_data (dict): The data after validation.

        Returns:
            User: The newly created User object.
        """
        fullname = validated_data.pop('fullname')
        repeated_pw = validated_data.pop('repeated_password')
        email = validated_data['email']
        password = validated_data['password']

        # Split fullname into first and last name
        name_parts = fullname.strip().split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        user = User(
            username=fullname,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user
