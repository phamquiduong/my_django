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
docker-compose --profile * down

@REM Build and up all services
echo ==================
echo Building and starting all docker services
docker-compose ^
    --profile server ^
    --profile database ^
    --profile mail_server ^
    --profile celery_worker ^
    up --build -d

@REM Migrate
echo ==================
echo Starting run migrate database
docker-compose exec django bash -c "python manage.py wait_for_db && python manage.py migrate"

@REM Collect static files
echo ==================
echo Starting collect Django statics file
docker-compose exec django python manage.py collectstatic --noinput
