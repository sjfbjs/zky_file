# -*- coding: utf-8 -*-
import djcelery
from datetime import timedelta

djcelery.setup_loader()

# 导入任务
CELERY_IMPORTS = [
    'index.tasks',
    'esutil.tasks'
]
# 设置队列-----可以无限加队列
CELERY_QUEUES = {
    'beat_tasks': {
        'exchange': 'beat_tasks',
        'exchange_type': 'direct',
        'binding_key': 'beat_tasks'
    },
    'test_tasks': {
        'exchange': 'test_tasks',
        'exchange_type': 'direct',
        'binding_key': 'test_tasks'
    },
    'estest_tasks': {
        'exchange': 'estest_tasks',
        'exchange_type': 'direct',
        'binding_key': 'estest_tasks'
    },

    'work_queue': {
        'exchange': 'work_queue',
        'exchange_type': 'direct',
        'binding_key': 'work_queue'
    }
}
# 设置默认列队,不符合其他队列的任务放在默认队列
CELERY_DEFAULT_QUEUE = 'work_queue'

# 有些情况下可以防止死锁
CELERYD_FORCE_EXECV = True

# 设置并发数量
CELERYD_CONCURRENCY = 4

# 每个worker最多执行100个任务，防止泄露内存
CELERYD_MAX_TASKS_PER_CHILD = 100

# 单个任务最多执行时间
CELERYD_TASK_TIME_LIMIT = 12 * 300

# 设置定时执行
# CELERYBAET_SCHEDULE = {
#     'task1': {
#         'task': 'test-task',
#         'schedule': timedelta(seconds=5),
#         'options': {
#             'queue': 'test_tasks'
#         }
#     }
# }

CELERY_ACCEPT_CONTENT = ['pickle', 'json', ]

BROKER_BACKEND = 'redis'
BROKER_URL = 'redis://192.168.1.252:6379/1'
CELERY_RESULT_BACKEND = 'redis://192.168.1.252:6379/2'
