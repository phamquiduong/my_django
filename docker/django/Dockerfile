FROM python:3.13-slim

# The stdout and stderr streams are sent straight to terminal (e.g. your container log
# without being first buffered and that you can see the output of your application (e.g. django logs) in real time.
ENV PYTHONUNBUFFERED=1

# Install Python package
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Load Vietnamese provinces database
COPY /resource /resource

# Setup environment variables
COPY /.env /.env

# Copy source code
WORKDIR /src
COPY /src /src

# Wait PostgreSQL and Redis then start server at port 8000
CMD bash -c "python manage.py wait_for_db \
             && python manage.py wait_for_redis \
             && gunicorn main.wsgi:application --bind 0.0.0.0:8000"
