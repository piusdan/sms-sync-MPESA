from celery import Celery
from celery.utils.log import get_task_logger

from config import Config

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

celery_logger = get_task_logger(__name__)
