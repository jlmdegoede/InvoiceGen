from __future__ import absolute_import, unicode_literals
import os
from InvoiceGen.settings import INSTALLED_APPS
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InvoiceGen.settings')

app = Celery('InvoiceGen', backend='redis')
app.config_from_object('django.conf:settings')
app.conf.broker_url = 'redis://localhost:6379/0'
app.autodiscover_tasks(lambda: INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
