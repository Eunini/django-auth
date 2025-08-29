# Django Authentication Service

A Django REST API with PostgreSQL, Redis, and JWT authentication.  
Supports user registration, login, profile, forgot/reset password with Redis-backed TTL tokens.

---

## 🚀 Live Demo

**[https://django-auth-j8gp.onrender.com/](https://django-auth-j8gp.onrender.com/)**

---

## 📦 Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/auth_service.git
cd auth_service
```

### 2. Install Dependencies

#### Using Docker (Recommended)
```bash
cp .env.example .env
docker compose up -d --build
```

#### Local Development (Python 3.10+)
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
pip install -r requirements.txt
cp .env.example .env
```

### 3. Run Migrations

#### Docker
```bash
docker compose exec web python manage.py migrate
```

#### Local
```bash
python manage.py migrate
```

### 4. Create Superuser

#### Docker
```bash
docker compose exec web python manage.py createsuperuser
```

#### Local
```bash
python manage.py createsuperuser
```

### 5. Start the Server

#### Docker
```bash
docker compose up
```

#### Local
```bash
python manage.py runserver
```

---

## ⚙️ Environment Variables

Set these in your `.env` file or Render dashboard:

| Variable      | Description                        | Example Value                                                      |
|---------------|------------------------------------|--------------------------------------------------------------------|
| `DATABASE_URL`| PostgreSQL connection string       | `postgres://user:pass@host:5432/dbname`                            |
| `REDIS_URL`   | Redis connection string            | `redis://localhost:6379/1`                                         |
| `SECRET_KEY`  | Django secret key                  | `your-very-secret-key`                                             |
| `DEBUG`       | Debug mode (True/False)            | `False`                                                            |
| `ALLOWED_HOSTS`| Allowed hosts (comma-separated)   | `127.0.0.1,localhost,yourdomain.com`                               |

---

## 📚 API Documentation

Interactive docs available at:  
**`/api/docs/`** (Swagger/OpenAPI UI)

### Endpoints

#### Register
- **POST** `/api/auth/register`
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "strongpassword123"
  }
  ```
- **Response:**
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe"
  }
  ```

#### Login
- **POST** `/api/auth/login`
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "strongpassword123"
  }
  ```
- **Response:**
  ```json
  {
    "access": "jwt-access-token",
    "refresh": "jwt-refresh-token"
  }
  ```

#### Profile (Me)
- **GET** `/api/auth/me`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe"
  }
  ```

#### Forgot Password
- **POST** `/api/auth/forgot-password`
- **Body:**
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response:**
  ```json
  {
    "detail": "Password reset email sent if user exists."
  }
  ```

#### Reset Password
- **POST** `/api/auth/reset-password`
- **Body:**
  ```json
  {
    "token": "reset-token-from-email",
    "password": "newstrongpassword123"
  }
  ```
- **Response:**
  ```json
  {
    "detail": "Password has been reset successfully."
  }
  ```

---

## 📝 Deployment

- **Live App:** [https://django-auth-j8gp.onrender.com/](https://django-auth-j8gp.onrender.com/)
- Deploy to [Render](https://render.com/) or [Railway](https://railway.app/) using Docker.
- Set all environment variables in the Render/Railway dashboard.
- After deployment, run:
  ```bash
  python manage.py migrate
  python manage.py collectstatic --noinput
  ```

---

## 🛠️ Tech Stack

- Django & Django REST Framework
- PostgreSQL
- Redis
- SimpleJWT
- Docker
- drf-spectacular (Swagger/OpenAPI docs)

---