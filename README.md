# 🗂️ KannMind Backend

![Django](https://img.shields.io/badge/Django-4.x+-green.svg)
![REST API](https://img.shields.io/badge/REST-API-blue.svg)
![License](https://img.shields.io/github/license/Getinger96/KannMind_Backend)

> **A modern Kanban board backend**, built with Django & Django REST Framework.  
> Provides a full-featured REST API for managing boards, lists (columns), and cards (tasks) — ideal for use with a separate frontend.

---

## 🚀 Features

- 🔐 User registration & authentication (Token/JWT/Session-based)
- 📋 Full CRUD operations for:
  - Boards
  - Lists (Columns)
  - Cards (Tasks)
- 👥 Permission system for private/shared boards
- 🧩 RESTful API structure for frontend integration
- ⚙️ Admin panel available at `/admin/`

---

## ⚙️ Tech Stack

- 🐍 Python 3.x  
- 🧬 Django 4.x+  
- 🔌 Django REST Framework  
- 🗄️ SQLite / PostgreSQL (configurable)  
- 🔐 JWT Authentication (`djangorestframework-simplejwt` - optional)

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Getinger96/KannMind_Backend.git
cd KannMind_Backend
```

---

### 2️⃣ Create and activate a virtual environment

```bash
python3 -m venv env
source env/bin/activate   
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Apply database migrations

```bash
python manage.py migrate
```

---


### 5️⃣ Create a superuser

```bash
python manage.py createsuperuser
```

---

### 6️⃣ Run the development server

```bash
python manage.py runserver
👉 API verfügbar unter: http://127.0.0.1:8000/
👉 Admin Panel unter: http://127.0.0.1:8000/admin/
```

----

## 📖 API Overview

The API supports managing:

- 🧩 Boards  
- 🗂️ Tasks   
- 💬 Comments   
- 👤 User authentication: Register & Login  

Use tools like Postman, Insomnia, or your frontend app to test and interact with the API.

---

## 🧪 Sample Endpoints

| Method | Endpoint                                | Description                            |
|--------|-----------------------------------------|----------------------------------------|
| POST   | `/api/registration/`                    | Register a new user                    |
| POST   | `/api/login/`                           | Log in a user                          |
| GET    | `/api/email-check/`                     | Check if an email is already in use    |

### Boards
| Method | Endpoint                                | Description                            |
|--------|-----------------------------------------|----------------------------------------|
| GET    | `/api/boards/`                          | Retrieve all boards                    |
| POST   | `/api/boards/`                          | Create a new board                     |
| GET    | `/api/boards/{board_id}/`               | Retrieve a specific board              |
| PATCH  | `/api/boards/{board_id}/`               | Update a specific board                |
| DELETE | `/api/boards/{board_id}/`               | Delete a specific board                |

### Tasks
| Method | Endpoint                                                | Description                            |
|--------|---------------------------------------------------------|----------------------------------------|
| GET    | `/api/tasks/assigned-to-me/`                            | Get tasks assigned to the user         |
| GET    | `/api/tasks/reviewing/`                                 | Get tasks the user is reviewing        |
| POST   | `/api/tasks/`                                           | Create a new task                      |
| PATCH  | `/api/tasks/{task_id}/`                                 | Update a specific task                 |
| DELETE | `/api/tasks/{task_id}/`                                 | Delete a specific task                 |
| GET    | `/api/tasks/{task_id}/comments/`                        | Get comments for a specific task       |
| POST   | `/api/tasks/{task_id}/comments/`                        | Add a comment to a task                |
| DELETE | `/api/tasks/{task_id}/comments/{comment_id}/`           | Delete a specific comment from a task  |


Full endpoint details are defined in your `urls.py` or browsable via the Django REST Framework interface.

---

## 📂 Project Structure (Quick Overview)

KannMind_Backend/
├── kannmind/ # Core app
│ ├── models.py # Data models
│ ├── views.py # API views
│ ├── serializers.py # DRF serializers
│ └── urls.py # API routing
├── manage.py
├── requirements.txt

---

## 🤝 Contributing

Pull requests are welcome!  
If you find a bug or have a suggestion, feel free to open an issue.

---

## 📄 License

MIT License © Getinger96

---

## 📬 Contact

For questions or collaboration:  
📘 [LinkedIn](https://www.linkedin.com/in/erich-getinger-45536a255/)







