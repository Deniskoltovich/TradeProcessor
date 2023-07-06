import os

from celery import Celery
from dotenv import load_dotenv

project_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
load_dotenv(os.path.join(project_dir, '.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('Core', include=['accounts.tasks'])
app.config_from_object('config.celery_config')
app.autodiscover_tasks(
    [
        'accounts.tasks',
    ]
)
CELERY_IMPORTS = ("accounts.tasks", "orders.tasks")

if __name__ == '__main__':
    app.start()
