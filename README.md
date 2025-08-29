# Django Authentication Service

A Django REST API with PostgreSQL, Redis, and JWT auth. Supports register, login, profile, forgot/reset password with Redis-backed TTL.  

## Features
- Django + DRF + SimpleJWT
- PostgreSQL database
- Redis cache for password reset tokens
- Rate limiting with DRF throttling
- Swagger/OpenAPI docs (`/api/docs/`)
- Dockerized (Postgres + Redis + Django)
- Deployment-ready for Railway/Render

## Endpoints
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/auth/forgot-password`
- `POST /api/auth/reset-password`

## Setup
```bash
cp .env.example .env
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser