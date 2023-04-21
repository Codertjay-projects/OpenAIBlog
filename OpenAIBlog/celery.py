import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OpenAIBlog.settings')

# used redis broker if it exists
app = Celery('OpenAIBlog', broker="redis://localhost:6379", backend="redis://localhost:6379")

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)
BROKER_URL = "redis://localhost:6379"
broker_url = "redis://localhost:6379"
app.conf.broker_url = BROKER_URL
CELERY_BROKER_URL = BROKER_URL

app.conf.beat_schedule = {
    # deleting customer models with no user associated and created over 10 days and no orders
    'delete_customer_in_active': {
        'task': 'blog.tasks.auto_get_datas',
        'schedule': crontab(hour=23, minute=0),
    },
}


@app.task
def debug_task():
    print(f'Request: ')
