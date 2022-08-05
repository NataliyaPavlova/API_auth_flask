## What is it:

Back-end for Auth service for online cinema

## What is in it:

1. Flask Auth API with signup, login, logout
2. Use of JWT access and refresh tokens
3. Flask API to get user's history of logins and use its profile
4. Flask CRUD API to manage roles
5. Tests (pytest) 

## How to start:

docker-compose up --build

## Before you start:

1. Migrate: 
```alembic upgrade head```
2. Create super-user:
```flask create_superuser password```

## Documentation

http://localhost:5000/

## How to test

docker-compose -f docker-compose.yml -f docker-compose.tests.yml up --build

## Roles and permissions:

1. admin
2. subscribed user
3. base
4. anonym

## Stack:

Flask, SQLAlchemy, PostgreSQL, Docker Compose, Redis, Pytest, alembic
