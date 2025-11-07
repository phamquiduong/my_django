@echo off

cd docker

@REM Create .env file if not exists
IF NOT EXIST .env (
    echo ==================
    echo .env file not found. Copying from .env.example...
    copy .env.example .env
)

@REM Down all services
echo ==================
echo Shuting down all docker services
docker-compose down

@REM Build and up all services
echo ==================
echo Building and starting all docker services
docker-compose up --build -d

@REM Wait DB starting up
echo ==================
docker-compose exec django python manage.py wait_for_db

@REM Migrate
echo ==================
echo Starting run migrate database
docker-compose exec django python manage.py migrate

@REM Collect static files
echo ==================
echo Starting collect Django statics file
docker-compose exec django python manage.py collectstatic --noinput
