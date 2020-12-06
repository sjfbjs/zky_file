# zky_file   django对接celery
# 使用django-celery组件


#启动celery任务
- 
* python.exe  manage.py  celery worker -l info
* 在tasks里面加入需要执行的任务
  #### 示例：     'test_tasks': {
        'exchange': 'test_tasks',
        'exchange_type': 'direct',
        'binding_key': 'test_tasks'
    },