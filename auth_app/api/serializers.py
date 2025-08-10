from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for representing User objects with an
    additional computed property 'fullname' that
    returns the combination of first and last name.
    """
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        """
        Returns the full name if available.
        If first and last names are empty, returns
        the username or email instead.
        """
        full = f"{obj.first_name} {obj.last_name}".strip()
        return full if full else obj.username or obj.email


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users with validation
    of email and password, including double password entry
    and splitting the provided 'fullname' into first and last names.
    """
    fullname = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """
        Validates that the email is not already taken.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate(self, data):
        """
        Validates that password and repeated password match.
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'error': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        """
        Creates a new User by splitting fullname into
        first and last names and hashing the password.
        """
        fullname = validated_data.pop('fullname')
        validated_data.pop('repeated_password')

        name_parts = fullname.strip().split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        user = User(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    """
    Serializer for authentication via email and password.
    Validates credentials and returns the user on success.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Checks if a user with the given email exists and
        if the password is correct.
        """
        user = User.objects.filter(email=data['email']).first()
        if not user:
            raise serializers.ValidationError('Invalid credentials')

        user = authenticate(username=user.username, password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')

        return {'user': user}
