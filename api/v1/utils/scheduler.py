import shutil
import subprocess
from celery import Celery
from falcon import status_codes as status
from celery_singleton import Singleton
from .ga import GeneticAlgorithm
import os

app = Celery('schedule',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')


@app.task(base=Singleton)
def schedule(data):
    ga = GeneticAlgorithm(data.get('rendimientos'),
                          data.get('pendientes'), data.get('kgs'))
    ga.run()
    solution = ga.get_solution_for_humans()
    return solution
    
