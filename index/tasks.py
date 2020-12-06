#coding:utf-8
__author__ = 'sjf'
import logging

from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
# from celerytask  import app


# @app.task
# def send_verification_email(user_id):
#     UserModel = get_user_model()
#     try:
#         user = UserModel.objects.get(pk=user_id)
#         send_mail(
#             'Verify your QuickPublisher account',
#             'Follow this link to verify your account: '
#             'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}),
#             'from@quickpublisher.dev',
#             [user.email],
#             fail_silently=False,
#         )
#     except UserModel.DoesNotExist:
#         logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
"""
    
    写入es的任务

"""
import time
from celery.task import Task

class Test():
    name = 'test-task'
    def run(self, *args, **kwargs):
        print('start es task...')
        time.sleep(3)
        print('args={args},kwargs={kwargs}')
        print('end es task....')

class EsImportFromFile(Task):
    name = 'es-task'
    def run(self, *args, **kwargs):
        print('start es task...')
        time.sleep(3)
        print('args={args},kwargs={kwargs}')
        print('end es task....')