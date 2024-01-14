from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

timezone = 'Pacific/Central'

CELERYBEAT_SCHEDULE = {
    'parse_weather_daily': {
        'task': 'celery_task.add',
        'schedule': crontab(hour='15', minute='30')
    }
}
