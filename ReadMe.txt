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

## Installation in Linux environment

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/videoflix-backend.git
   cd videoflix-backend

2. Create and activate a virtual environment:
    python3 -m venv env
    source env/bin/activate  # Linux/MacOS

3. Install dependencies:
    pip install -r requirements.txt # Linux

4. Set up the environment variables (see Environment Variables).
    Create a .env file in the project root and add the following configurations:
        EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST='your-email-smtp-host'
        EMAIL_PORT=587
        EMAIL_USE_TLS=True
        EMAIL_HOST_USER='your-email@example.com'
        EMAIL_HOST_PASSWORD='your-email-password'
        DEFAULT_FROM_EMAIL='your-email@example.com'

5. Update in settings.py
    ALLOWED_HOSTS = ['127.0.0.1', 'your_domains']

    CORS_ALLOWED_ORIGINS = ['http://localhost:4200','yor_frontend_url']

    for PostgreSQL:
      DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'videoflix',
            'USER': 'YourName',
            'PASSWORD': 'YourPassword',
            'HOST': 'localhost',
            'PORT': '5432'
        }
      }

6. Install FFmpeg
    sudo apt update
    sudo apt install ffmpeg -y

7. Run migrations:
    python manage.py makemigrations
    python manage.py migrate

8. Configure your deploaments
    #Nginx
      write in Terminal: sudo nano /etc/nginx/sites-available/default
        Insert the following content:

          server {
             listen 80;
             listen 443;
             server_name 127.0.0.1;
             location / {
              include proxy_params;
              proxy_pass http://127.0.0.1:8000;
             }
          }          

    #Supervisor
      write in Terminal with your project name: nano /etc/supervisor/conf.d/videoflix_gunicorn.conf
        Insert the following content:
        [program:videoflix_gunicorn]
        user=root
        directory=/root/Videoflix_backend/videoflix
        command=/root/Videoflix_backend//env/bin/gunicorn videoflix.wsgi:application --bin 127.0.0.1:8000 --workers 3
        autostart=true
        autorestart=true
        stdout_logfile=/var/log/videoflix/gunicorn.log
        stderr_logfile=/var/log/videoflix/gunicorn.err.log
      create logfiles:
        sudo mkdir /var/log/videoflix/
        sudo touch /var/log/videoflix/gunicorn.log
        sudo touch /var/log/videoflix/gunicorn.err.log

    start Nginx 
      sudo service nginx start
    start Gunicorn
      gunicorn videoflix.wsgi:application --bin 127.0.0.1:8000 --workers 3
    start Supervisor
      sudo service supervisor start
      sudo supervisorctl start videoflix_gunicorn
    
  #Commands 
    for Nginx:
      sudo service nginx
                          start
                          stop
                          restart
    for Supervisor
      sudo supervisorctl
                          start videoflix_gunicorn
                          status videoflix_gunicorn
                          stop videoflix_gunicorn
                          restart videoflix_gunicorn

9. Configure PostgreSQL
    Start PostgreSQL
      sudo service postgresql
    Create database
      sudo su postgres
      psql
    Insert the following content with your data:
      CREATE DATABASE myproject;
      CREATE USER myprojectuser WITH PASSWORD 'password';
      ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
      ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
      ALTER ROLE myprojectuser SET timezone TO 'UTC';
      GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;

10. Install Letsencrypt
    #create a DNS on your FTP server with an IP address of the backend server
      sudo apt install letsencrypt
      sudo systemctl status certbot.timer
      sudo apt install python3-certbot-nginx
    #Without Nginx
      sudo certbot certonly --standalone --agree-tos --preferred-challenges http -d meine-domain.de --register-unsafely-without-email
    #Or
      sudo certbot certonly --manual --agree-tos --preferred-challenges dns -d meine-domain.de -d *.meine-domain.de
    #Or (best)
      sudo certbot --nginx --nginx-server-root /etc/nginx/sites-enabled/ -d meine-domain.de -d *.meine-domain.de --agree-tos
    #update Nginx config
      sudo nano /etc/nginx/sites-enabled/default
      Insert the following content:
        server {
            listen 80;
            server_name deine.domain.com;                                                     #enter your domain here
            rewrite     ^   https://$server_name$request_uri? permanent;
        }

        server {
            listen 443 default_server ssl;
            server_name 127.0.0.1;

            ssl_certificate /etc/letsencrypt/live/deine.domain.com/fullchain.pem;               #enter your domain here
            ssl_certificate_key /etc/letsencrypt/live/deine.domain.com/privkey.pem;             #enter your domain here

            location / {
                include proxy_params;
                proxy_pass http://127.0.0.1:8000;
            }
        }

##API Documentation

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