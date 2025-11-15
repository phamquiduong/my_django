FROM python:3.13-slim

RUN pip install --no-cache-dir celery[redis] flower

CMD bash -c "celery \
             --broker=${CELERY_FLOWER_BROKER} \
             --result-backend=${CELERY_FLOWER_RESULT_BACKEND} \
             flower --port=5555"
