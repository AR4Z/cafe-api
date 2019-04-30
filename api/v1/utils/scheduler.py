import shutil
import subprocess
from celery import Celery
from falcon import status_codes as status
from celery_singleton import Singleton
from dynaconf import settings
from .utils import RedisService

app = Celery('cloner',
                    broker=settings.get('CELERY_BROKER'),
                    backend=settings.get('CELERY_BACKEND'))

service = RedisService()


@app.task(base=Singleton)
def schedule(data):
    
