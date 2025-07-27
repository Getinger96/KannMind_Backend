# Importiert das Standard-User-Modell von Django zur Nutzung in Beziehungen
from django.contrib.auth.models import User
# Importiert das Modulsystem von Django zum Erstellen eigener Datenbankmodelle
from django.db import models


# Definiert ein benutzerdefiniertes Profilmodell, das zusätzliche Informationen zum User speichert
class UserProfile(models.Model):
    # Erstellt eine Eins-zu-eins-Beziehung zum eingebauten User-Modell.
    # Wenn der User gelöscht wird, wird auch das zugehörige Profil gelöscht.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Optionales Textfeld für die Biografie des Users
    bio = models.TextField(blank=True, null=True)
    
    # Optionales Feld für den Standort des Users, max. 100 Zeichen
    location = models.CharField(max_length=100, blank=True, null=True)

    # Gibt den Benutzernamen zurück, wenn das Profil als String dargestellt wird
    def __str__(self):
        return self.user.username