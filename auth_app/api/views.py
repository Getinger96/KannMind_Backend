from rest_framework import generics
from auth_app.models import UserProfile
from .serializers import UserProfileSerializer, RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer




class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]


    def post(self,request):
        serializer= self.serializer_class(data = request.data)

        data={}

        if serializer.is_valid():
            user= serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data={
                'token':token.key,
                'username':user.username,
                'email':user.email,
                'user_id':user.pk

            }
        else:
            data=serializer.errors
        
        return Response(data)




class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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
