import psycopg2
import datetime
from celery import Celery
from celery.schedules import crontab

app = Celery('celery_task',
             broker='redis://localhost:6379/0')

@app.celery_task
def add(x,y):
    return x + y

