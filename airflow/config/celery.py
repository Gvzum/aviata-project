from celery import Celery
from celery.schedules import crontab

from config import settings

"""
     celery -A config.celery worker --loglevel=INFO  
     celery -A config.celery beat --loglevel=info 
     celery call tasks.update_currency
     uvicorn --reload --port 8009 provider_b.main:app
     uvicorn --reload --port 8008 provider_a.main:app
     uvicorn --reload --port 9000 main:app 
"""

app = Celery("aviata")
app.config_from_object("config.settings:settings")
app.autodiscover_tasks()

from tasks import *  # noqa

app.conf.beat_schedule = {
    'update_currency': {
        'task': 'tasks.update_currency',
        'schedule': crontab(hour=12, minute=0),
    }
}
