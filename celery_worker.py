import os

from app import create_app
from app.celery_cfg import celery

app = create_app(os.getenv('USSD_CONFIG') or 'default')
app.app_context().push()

celery.conf.update(app.config)