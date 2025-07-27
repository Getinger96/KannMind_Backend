# Importiert die Basisklasse für App-Konfigurationen von Django
from django.apps import AppConfig


# Definiert die Konfiguration für die Django-App 'auth_app'
class AuthAppConfig(AppConfig):
    # Gibt an, welcher AutoField-Typ standardmäßig für automatisch erstellte Primärschlüssel verwendet wird
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Der Name der App – muss mit dem Ordnernamen in deinem Projekt übereinstimmen
    name = 'auth_app'
