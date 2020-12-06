#coding:utf-8
__author__ = 'sjf'
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zky_file.settings')

app = Celery('zky_file')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()