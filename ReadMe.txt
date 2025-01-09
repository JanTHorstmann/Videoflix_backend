# Videoflix Backend

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation](#installation)
5. [Environment Variables](#environment-variables)
6. [Database Setup](#database-setup)
7. [API Documentation](#api-documentation)

---

## Project Overview
Videoflix is a backend service designed to support a video streaming platform. 
It handles user registration, video storage and retrieval, as well as tracking video progress for users.

---

## Features
- User registration and email confirmation.
- Storage and retrieval of video content.
- Tracking and saving users' video progress.
- High performance with Redis and task queuing via Django RQ.

---

## Technologies Used
- **Framework:** Django
- **Database:** PostgreSQL
- **Task Queue:** Redis and Django RQ
- **Deployment:** Nginx, Gunicorn, Supervisor

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/videoflix-backend.git
   cd videoflix-backend

2. Create and activate a virtual environment:
    python3 -m venv env
    source env/bin/activate  # Linux/MacOS
    env\Scripts\activate     # Windows

3. Install dependencies:
    pip install -r requirements.txt     # Windows
    pip install -r requirements_lin.txt # Linux

4. Set up the environment variables (see Environment Variables).
    Create a .env file in the project root and add the following configurations:
        EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST='your-email-smtp-host'
        EMAIL_PORT=587
        EMAIL_USE_TLS=True
        EMAIL_HOST_USER='your-email@example.com'
        EMAIL_HOST_PASSWORD='your-email-password'
        DEFAULT_FROM_EMAIL='your-email@example.com'

5. Run migrations:
    python manage.py makemigrations
    python manage.py migrate

6. Start the development server:
    python manage.py runserver


Database Setup

PostgreSQL is used for this project. To set up the database on a Linux environment, use the following commands:
    CREATE DATABASE myproject;
    CREATE USER myprojectuser WITH PASSWORD 'password';
    ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
    ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
    ALTER ROLE myprojectuser SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;


API Documentation

User Registration

Endpoint: POST /api/register/
Description: Registers a new user and sends a confirmation email.

Request Body:
    {
      "username": "john_doe",
      "email": "john.doe@example.com",
      "password": "securepassword"
    }

Response:
    {
      "message": "Registration successful. Please check your email to confirm your account."
    }

Video Content Retrieval

Endpoint: GET /api/videos/
Description: Retrieves a list of all available videos.

Response:
    [
      {
        "id": 1,
        "title": "Introduction to Videoflix",
        "description": "Welcome to Videoflix!",
        "thumbnail": "http://example.com/thumbnail1.jpg",
        "created_at": "2023-12-01T12:34:56Z"
      }
    ]

Save Video Progress

Endpoint: POST /api/videos/progress/
Description: Saves the user's progress for a video.

Request Body:
    {
      "video_id": 1,
      "played_time": 120
    }

Response:
    {
      "message": "Progress saved successfully."
    }


Contribution

Feel free to open issues or submit pull requests to contribute to this project.


License

This project is for personal or educational use and does not include a license. Please contact the author for more information.