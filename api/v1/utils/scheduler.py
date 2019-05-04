import shutil
import subprocess
from celery import Celery
from falcon import status_codes as status
from celery_singleton import Singleton
from .ga import GeneticAlgorithm
import os

app = Celery('schedule',
             broker=os.environ['REDIS_URL'],
             backend=os.environ['REDIS_URL'])


@app.task(base=Singleton)
def schedule(data):
    ga = GeneticAlgorithm(data.get('rendimientos'),
                          data.get('pendientes'), data.get('kgs'))
    ga.run()
    return ga.get_solution_for_humans()
