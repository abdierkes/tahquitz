import psycopg2
import datetime
from celery import Celery
from celery.schedules import crontab

# app = Celery('celery_task',
#              broker='redis://localhost:6379/0')

app = Celery('celery_task')
app.config_from_object('celery_config')

@app.task
def add(x,y):
    return x + y

