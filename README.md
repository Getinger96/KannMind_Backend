🗂️ KannMind_Backend
This is the backend of a Kanban board application, developed with Django. It provides a RESTful API for managing boards, lists, and cards (tasks).

🚀 Features
User registration & authentication (token-based/session-based)

CRUD operations for:

Boards

Lists / Columns

Cards / Tasks

Permission management (e.g., private/shared boards)

API-based communication suitable for separate frontend apps

Admin interface available at /admin/

⚙️ Technology Stack
Python 3.x

Django 4.x+

Django REST Framework (DRF)

SQLite / PostgreSQL (configurable)

(Optional) JWT / Token authentication using djangorestframework-simplejwt

🛠️ Setup & Installation
Follow these steps to get the project running locally:

Clone the repository

bash
Kopieren
Bearbeiten
git clone https://github.com/Getinger96/KannMind_Backend.git
cd KannMind_Backend
Create and activate a virtual environment (recommended)

bash
Kopieren
Bearbeiten
python3 -m venv env
source env/bin/activate      # On Windows: env\Scripts\activate
Install dependencies

bash
Kopieren
Bearbeiten
pip install -r requirements.txt
Configure environment variables

Create a .env file or set environment variables for sensitive data, for example:

ini
Kopieren
Bearbeiten
DJANGO_SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3   # Or your PostgreSQL connection URL
Alternatively, configure settings.py to read from these environment variables.

Apply database migrations

bash
Kopieren
Bearbeiten
python manage.py migrate
Create a superuser for admin access

bash
Kopieren
Bearbeiten
python manage.py createsuperuser
Follow the prompts to create your admin account.

Run the development server

bash
Kopieren
Bearbeiten
python manage.py runserver
The API will be accessible at: http://127.0.0.1:8000/

Access the Django admin interface

Open your browser and go to http://127.0.0.1:8000/admin/
Log in with the superuser credentials created earlier.

📖 API Documentation
The API provides endpoints for managing boards, tasks, comments, and user authentication (registration/login).
Use tools like Postman or your frontend application to interact with the API.