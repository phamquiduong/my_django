@echo off

cd docker
IF NOT EXIST .env (
    echo .env file not found. Copying from .env.example...
    copy .env.example .env
)

@REM Create super user
docker-compose exec django python manage.py createsuperuser
