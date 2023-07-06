import os

accept_content = ['json']

broker_url = os.environ.get('BROKER_REDIS_URL')
task_always_eager = int(
    os.environ.get('CELERY_TASKS_ALWAYS_EAGER')  # type: ignore
)  # type: ignore
task_serializer = 'json'
task_default_queue = 'default'
