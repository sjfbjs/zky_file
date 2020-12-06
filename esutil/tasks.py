#coding:utf-8
__author__ = 'sjf'
import logging

from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
# from celerytask  import app
"""    
    写入es的任务

"""
import time
from celery.task import Task
#初步完成异步任务改造
class Test(Task):
    name = 'estest-task'
    def run(self, *args, **kwargs):
        print('start esutil es task...')
        time.sleep(3)
        print('args=' +  str(*args) + ' kwargs=' )
        print('end esutil es  task....')

