# config celery

import os

import django
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings.dev')
app = Celery('storefront')

# go to the django.conf module and load the settings object
# don't get why use colon here,
# this importing or referencing syntax is not supported by python
# <? it looks like a custom rule defined in celery ?>
# this writing applies to this method 'config_from_object', the ':settings'
# specifies the configuration object.
app.config_from_object('django.conf:settings', namespace='CELERY')
# instruct celery to automatically discover all the tasks in tasks module
app.autodiscover_tasks()



# import os
#
# from celery import Celery
#
# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
#
# app = Celery('proj')
#
# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Load task modules from all registered Django apps.
# app.autodiscover_tasks()