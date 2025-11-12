FROM python:3.13-slim

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY /docker/.env /.env

WORKDIR /src
COPY /src /src

CMD bash -c "python manage.py wait_for_db \
             && python manage.py wait_for_redis \
             && celery -A main flower --port=5555"
