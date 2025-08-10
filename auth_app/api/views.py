from .serializers import  RegistrationSerializer,CustomAuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status

class CustomLoginView(ObtainAuthToken):
    """
    View zur Authentifizierung von Nutzern via E-Mail und Passwort.
    Verwendet den CustomAuthTokenSerializer zur Validierung der Credentials.
    Gibt bei erfolgreicher Anmeldung ein Auth-Token sowie
    Nutzerinformationen (vollständiger Name, E-Mail, User-ID) zurück.
    """
    permission_classes = [AllowAny]
    serializer_class = CustomAuthTokenSerializer

    def post(self, request):
        """
        Verarbeitet POST-Anfragen mit den Login-Daten.
        Validiert die Daten, erstellt (oder holt) ein Token für den User
        und gibt dieses zusammen mit Nutzerinformationen zurück.
        Bei ungültigen Daten wird ein Fehlerstatus mit Fehlermeldungen gesendet.
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
    View zur Registrierung neuer Nutzer.
    Nimmt die Nutzerdaten entgegen, validiert diese und legt
    bei Erfolg einen neuen User an.
    Gibt anschließend ein Auth-Token und Nutzerinformationen zurück.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Verarbeitet POST-Anfragen mit Registrierungsdaten.
        Validiert und speichert den neuen Nutzer.
        Erstellt (oder holt) ein Token für den neuen User und gibt
        dieses mit Nutzerinformationen zurück.
        Bei Fehlern in den Daten wird ein Fehlerstatus mit Details gesendet.
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
