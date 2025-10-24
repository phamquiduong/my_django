@echo off

cd docker
IF NOT EXIST .env (
    echo .env file not found. Copying from .env.example...
    copy .env.example .env
)

docker-compose down
docker-compose up --build -d

@REM Migrate
docker-compose exec django python manage.py migrate

@REM Collect static files
docker-compose exec django python manage.py collectstatic --noinput
