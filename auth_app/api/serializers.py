from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer zur Darstellung von User-Objekten mit einer
    zusätzlichen berechneten Eigenschaft 'fullname', die
    Vor- und Nachname kombiniert zurückgibt.
    """
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        """
        Gibt den vollständigen Namen zurück, falls vorhanden.
        Falls Vor- und Nachname leer sind, wird der
        Benutzername oder die E-Mail verwendet.
        """
        full = f"{obj.first_name} {obj.last_name}".strip()
        return full if full else obj.username or obj.email


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer zur Registrierung neuer Nutzer mit Validierung
    von E-Mail und Passwort, inklusive doppelter Passwortabfrage
    und Aufteilung des übergebenen 'fullname' in Vor- und Nachname.
    """
    fullname = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """
        Validiert, dass die E-Mail noch nicht vergeben ist.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate(self, data):
        """
        Validiert, dass Passwort und wiederholtes Passwort übereinstimmen.
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'error': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        """
        Erstellt einen neuen User, indem der fullname in Vor- und Nachname
        zerlegt wird und das Passwort gehasht gespeichert wird.
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
    Serializer für die Authentifizierung via E-Mail und Passwort.
    Validiert die Credentials und gibt bei Erfolg den User zurück.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Prüft, ob ein User mit der angegebenen E-Mail existiert und
        ob das Passwort korrekt ist.
        """
        user = User.objects.filter(email=data['email']).first()
        if not user:
            raise serializers.ValidationError('Invalid credentials')

        user = authenticate(username=user.username, password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')

        return {'user': user}