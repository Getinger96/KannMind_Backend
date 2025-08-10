from .serializers import  RegistrationSerializer,CustomAuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status

class CustomLoginView(ObtainAuthToken):
    """
    View for authenticating users via email and password.
    Uses CustomAuthTokenSerializer to validate credentials.
    On successful login, returns an auth token along with
    user information (full name, email, user ID).
    """
    permission_classes = [AllowAny]
    serializer_class = CustomAuthTokenSerializer

    def post(self, request):
        """
        Handles POST requests with login data.
        Validates the data, creates (or retrieves) a token for the user,
        and returns it along with user info.
        Returns an error status with messages if data is invalid.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            fullname = f"{user.first_name} {user.last_name}".strip()
            return Response({
                'token': token.key,
                'fullname': fullname,
                'email': user.email,
                'user_id': user.pk
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(APIView):
    """
    View for registering new users.
    Accepts user data, validates it, and creates
    a new user upon success.
    Returns an auth token and user info afterwards.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST requests with registration data.
        Validates and saves the new user.
        Creates (or retrieves) a token for the new user and returns
        it along with user information.
        Returns an error status with details if data is invalid.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            fullname = f"{user.first_name} {user.last_name}".strip()

            return Response({
                'token': token.key,
                'fullname': fullname,
                'email': user.email,
                'user_id': user.pk
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
