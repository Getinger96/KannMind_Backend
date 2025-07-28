from rest_framework import generics
from auth_app.models import UserProfile
from .serializers import UserProfileSerializer, RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken


class UserProfileList(generics.ListCreateAPIView):
    """
    API view to list all user profiles or create a new one.

    GET: Returns a list of all UserProfile instances.
    POST: Creates a new UserProfile instance.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific user profile.

    GET: Retrieves a single UserProfile by ID.
    PUT/PATCH: Updates the specified UserProfile.
    DELETE: Deletes the specified UserProfile.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CustomLoginView(ObtainAuthToken):
    """
    Custom login view that returns an authentication token along with user details.

    POST:
        Authenticates the user using their username and password.
        If valid, returns an auth token, username, email, and user ID.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST request for user login.

        Args:
            request (Request): The incoming HTTP request containing login credentials.

        Returns:
            Response: A response with either user token and info or validation errors.
        """
        serializer = self.serializer_class(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.pk
            }
        else:
            data = serializer.errors

        return Response(data)


class RegistrationView(APIView):
    """
    API view to register a new user.

    POST:
        Accepts user registration data (fullname, email, password).
        Creates a new User instance and returns an auth token along with user details.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST request for user registration.

        Args:
            request (Request): The incoming HTTP request containing registration data.

        Returns:
            Response: A response with either a success payload including token and user info,
                      or validation errors.
        """
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)

            fullname = f"{saved_account.first_name} {saved_account.last_name}".strip()

            data = {
                'token': token.key,
                'fullname': fullname,
                'email': saved_account.email,
                'user_id': saved_account.pk
            }
        else:
            data = serializer.errors

        return Response(data)
