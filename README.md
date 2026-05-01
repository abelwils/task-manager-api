#  TaskPro - Backend Developer Internship Assignment

## 📌 Overview

TaskPro is a scalable REST API with authentication and role-based access, built as part of a backend developer internship assignment.
It includes a secure backend with JWT authentication and a simple frontend UI to interact with the APIs.

---

##  Tech Stack

### Backend

* FastAPI
* SQLAlchemy (ORM)
* SQLite (can be replaced with PostgreSQL/MySQL)
* JWT Authentication (`python-jose`)
* Password hashing (`passlib`)

### Frontend

* Vanilla HTML, CSS, JavaScript

---

## ✨ Features

### Authentication

* User registration with password hashing
* Secure login with JWT tokens
* Token-based protected routes

### Role-Based Access

* User role (default)
* Admin role (can delete any task)

### 📦 Task Management (CRUD)

* Create tasks
* Read tasks (user-specific)
* Update tasks
* Delete tasks
* Toggle completion

### 🌐 Frontend UI

* Register & login users
* Dashboard with task management
* Create, edit, delete tasks
* Shows API responses (success/error)

---

## Security Features

* Password hashing using bcrypt
* JWT-based authentication
* Protected API routes
* Input validation with Pydantic

---

## 📁 Project Structure

```id="pj3m7f"
backend-project/
│
├── frontend/
│   └── index.html
│
├── main.py
├── models.py
├── schemas.py
├── auth.py
├── utils.py
├── database.py
├── README.md
```

---

##  Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/abelwils/taskpro.git
cd taskpro
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy python-jose passlib[bcrypt]
```

---

### 4️⃣ Run the server

```bash
uvicorn main:app --reload
```

---

### 5️⃣ Open in browser

```
http://127.0.0.1:8000
```

---

### 📄 API Documentation

Swagger UI available at:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Auth

* `POST /register` → Register user
* `POST /login` → Login & get JWT

### Tasks

* `POST /tasks` → Create task
* `GET /tasks` → Get user tasks
* `PUT /tasks/{id}` → Update task
* `DELETE /tasks/{id}` → Delete task
* `PATCH /tasks/{id}/complete` → Toggle completion

### Admin

* `DELETE /admin/tasks/{id}` → Delete any task (admin only)

---

## 📊 Database Schema

### User

* id
* email
* password
* role

### Task

* id
* title
* priority
* due_date
* completed
* created_at
* owner_id

---

## Scalability Notes

This project is designed with scalability in mind:

* Modular architecture (auth, models, routes separated)
* Can be extended to microservices (auth service, task service)
* Database can be migrated to PostgreSQL or MySQL
* Can integrate Redis for caching frequently accessed data
* Can be containerized using Docker
* Load balancing can be added using NGINX

---

## 👨‍💻 Author

Abel Wils

---

## 🎯 Conclusion

This project demonstrates secure API development, database design, authentication, and frontend integration — aligning with real-world backend engineering practices.
