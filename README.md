🗂️ KannMind Backend




A modern Kanban board backend, built with Django & Django REST Framework.
Provides a full-featured REST API for managing boards, lists (columns), and cards (tasks) — ideal for use with a separate frontend.

🚀 Features
🔐 User registration & authentication (Token/JWT/Session-based)

📋 Full CRUD operations for:

Boards

Lists (Columns)

Cards (Tasks)

👥 Permission system for private/shared boards

🧩 RESTful API structure for frontend integration

⚙️ Admin panel available at /admin/

⚙️ Tech Stack
🐍 Python 3.x

🧬 Django 4.x+

🔌 Django REST Framework

🗄️ SQLite / PostgreSQL (configurable)

🔐 JWT Authentication (djangorestframework-simplejwt - optional)

🛠️ Installation & Setup
1️⃣ Clone the repository
bash
Kopieren
Bearbeiten
git clone https://github.com/Getinger96/KannMind_Backend.git
cd KannMind_Backend
2️⃣ Create and activate a virtual environment
bash
Kopieren
Bearbeiten
python3 -m venv env
source env/bin/activate        # On Windows: env\Scripts\activate
3️⃣ Install dependencies
bash
Kopieren
Bearbeiten
pip install -r requirements.txt
4️⃣ Configure environment variables
Create a .env file in the project root:

env
Kopieren
Bearbeiten
DJANGO_SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3   # Or use your PostgreSQL URL
⚠️ Make sure your settings.py reads from environment variables (e.g. using os.environ or python-decouple).

5️⃣ Apply database migrations
bash
Kopieren
Bearbeiten
python manage.py migrate
6️⃣ Create a superuser
bash
Kopieren
Bearbeiten
python manage.py createsuperuser
Follow the prompts to create an admin account.

7️⃣ Run the development server
bash
Kopieren
Bearbeiten
python manage.py runserver
👉 API available at: http://127.0.0.1:8000/
👉 Admin panel at: http://127.0.0.1:8000/admin/

📖 API Overview
The API supports managing:

🧩 Boards

🧱 Lists (Columns)

🗂️ Cards (Tasks)

💬 Comments (if implemented)

👤 User authentication: Register & Login

Use tools like Postman, Insomnia, or your frontend app to test and interact with the API.

🧪 Sample Endpoints
Method	Endpoint	Description
GET	/api/boards/	Retrieve all boards
POST	/api/boards/	Create a new board
GET	/api/lists/<board_id>/	Get lists for a board
POST	/api/cards/	Create a new card/task
POST	/api/auth/login/	Log in a user

Full endpoint details are defined in your urls.py or browsable via the Django REST Framework interface.

📂 Project Structure (Quick Overview)
bash
Kopieren
Bearbeiten
KannMind_Backend/
├── kannmind/           # Core app
│   ├── models.py       # Data models
│   ├── views.py        # API views
│   ├── serializers.py  # DRF serializers
│   └── urls.py         # API routing
├── manage.py
├── requirements.txt
└── .env                # Environment variables (DO NOT commit)
🤝 Contributing
Pull requests are welcome!
If you find a bug or have a suggestion, feel free to open an issue.

📄 License
MIT License © Getinger96

📬 Contact
For questions or collaboration:
📘 LinkedIn

