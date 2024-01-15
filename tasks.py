import psycopg2
import datetime
from celery import Celery
from celery.schedules import crontab

app = Celery('tasks',
             broker='redis://localhost:6379',
             backend='redis://localhost:6379')


@app.on_after_configure.connect
def schedule_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, add.s(4, 4))


app.task(bind=True)


def add(x, y):
    print(x, y)
    return x + y
