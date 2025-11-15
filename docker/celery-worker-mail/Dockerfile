FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY /.env /.env

WORKDIR /src
COPY /src /src

CMD bash -c "celery -A main worker -n email@%h -l INFO -Q ${CELERY_EMAIL_QUEUE}"
