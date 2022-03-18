from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.conf import settings
import os

from pytz import timezone 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsProject.settings')
app = Celery('newsProject')
app.conf.enable_utc = False

# Optional configuration, see the application user guide.
app.conf.update(
    timezone = 'Asia/Kolkata'
)

app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))