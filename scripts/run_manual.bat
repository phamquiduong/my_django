@echo off

@REM Install requirements
echo ==================
echo Install Python packages
python.exe -m pip install --upgrade pip
pip install -r requirements.txt

@REM Create django environment file if not exists
IF NOT EXIST .env (
    echo ==================
    echo .env file not found. Copying from .env.example...
    copy .env.example .env
)

cd src

@REM Migrate
echo ==================
echo Starting run migrate database
python manage.py migrate

@REM Run server at port 80. Visit http://localhost
echo ==================
echo Running server
python manage.py runserver 0.0.0.0:80
