# 🗂️ Django KannMind_Backend Backend

Dies ist das Backend eines Kanban-Board-Projekts, entwickelt mit dem [Django](https://www.djangoproject.com/) Web-Framework. Es stellt eine RESTful API zur Verfügung, mit der Boards, Listen und Karten verwaltet werden können.

## 🚀 Features

- Benutzerregistrierung & Authentifizierung (Token-basiert / Session-basiert)
- CRUD für:
  - Boards
  - Listen / Spalten
  - Karten / Tasks
- Rechtemanagement (z. B. private / gemeinsame Boards)
- API-basierte Kommunikation (z. B. für ein separates Frontend)
- Admin-Oberfläche über `/admin/`

## ⚙️ Technologie-Stack

- Python 3.x
- Django 4.x+
- Django REST Framework (DRF)
- SQLite / PostgreSQL (je nach Konfiguration)
- (Optional) JWT / Token Auth mit `djangorestframework-simplejwt`

## 🛠️ Installation & Setup

1. Projekt klonen:

```bash
git clone https://github.com/Getinger96/KannMind_Backend
cd kanban-backend
Virtuelle Umgebung erstellen:

bash
Kopieren
Bearbeiten
python -m venv venv
source venv/bin/activate  # auf Windows: venv\Scripts\activate
Abhängigkeiten installieren:

bash
Kopieren
Bearbeiten
pip install -r requirements.txt
Migrationen anwenden:

bash
Kopieren
Bearbeiten
python manage.py migrate
Admin-Benutzer erstellen (optional):

bash
Kopieren
Bearbeiten
python manage.py createsuperuser
Server starten:

bash
Kopieren
Bearbeiten
python manage.py runserver
🔗 Standardmäßig läuft das Backend auf: http://127.0.0.1:8000/



