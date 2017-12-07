web: gunicorn manage:app --reload
worker: celery worker -A celery_worker.celery --loglevel=INFO