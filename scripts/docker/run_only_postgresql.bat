@echo off

cd docker

@REM Create .env file if not exists
IF NOT EXIST .env (
    echo .env file not found. Copying from .env.example...
    copy .env.example .env
)

@REM Down all services
docker-compose down

@REM Build and up PostgreSQL
docker-compose up postgresql --build -d
