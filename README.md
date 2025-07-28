🗂️ Django KannMind_Backend
This is the backend of a Kanban board project, developed using the Django web framework. It provides a RESTful API for managing boards, lists, and cards (tasks).

🚀 Features
User registration & authentication (token-based / session-based)

CRUD operations for:

Boards

Lists / Columns

Cards / Tasks

Permission management (e.g., private/shared boards)

API-based communication (e.g., for a separate frontend)

Admin interface available at /admin/

⚙️ Technology Stack
Python 3.x

Django 4.x+

Django REST Framework (DRF)

SQLite / PostgreSQL (configurable)

(Optional) JWT / Token authentication with djangorestframework-simplejwt

🛠️ Setup & Installation
Follow these steps to get the project up and running locally:

1. Clone the repository
bash
Kopieren
Bearbeiten
git clone https://github.com/Getinger96/KannMind_Backend.git
cd kannmind_backend
2. Create a virtual environment (recommended)
bash
Kopieren
Bearbeiten
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
3. Install dependencies
bash
Kopieren
Bearbeiten
pip install -r requirements.txt
4. Configure environment variables
Create a .env file or set environment variables for sensitive data, e.g.,

ini
Kopieren
Bearbeiten
DJANGO_SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3  # or your PostgreSQL URL
Alternatively, configure settings.py to read from these variables.

5. Apply migrations
bash
Kopieren
Bearbeiten
python manage.py migrate
6. Create a superuser (for admin access)
bash
Kopieren
Bearbeiten
python manage.py createsuperuser
Follow the prompts to create an admin account.

7. Run the development server
bash
Kopieren
Bearbeiten
python manage.py runserver
The API will be available at http://127.0.0.1:8000/

8. Access the admin interface
Navigate to http://127.0.0.1:8000/admin/ and log in with your superuser credentials.

📖 API Documentation
The API endpoints support CRUD operations on boards, tasks, comments, and user registration/login. Use tools like Postman or your frontend to interact with the API.

