FROM python:3.13-slim

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY docker/.env .env

COPY src/ src/
WORKDIR /src

CMD [ "gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:8000" ]
