from time import sleep
# from storefront.celery import app
from celery import shared_task

# To execute this function with celery,
# we need to decorate it with celery decorators

# with this approach
# the playground app is dependent on storefront folder
# @app.task


@shared_task
def notify_customers(message):
    print('Sending 10k emails')
    print(message)
    sleep(10)
    print('Emails were successfully sent')
