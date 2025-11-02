@echo off

@REM Install requirements
pip install -r requirements.txt
cls

@REM Create .env file if not exists
IF NOT EXIST .env (
    echo .env file not found. Copying from .env.example...
    copy .\docker\.env.example .env
)

cd src

@REM Wait for the database connection
python manage.py wait_for_db

@REM Migrate
python manage.py migrate

@REM Collect static files
python manage.py collectstatic --noinput

@REM Run server at port 80. Visit http://localhost
python manage.py runserver 0.0.0.0:80
