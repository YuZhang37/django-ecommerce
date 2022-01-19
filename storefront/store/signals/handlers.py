from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from store.models import Customer



# With post_save on User, we shift the responsibility of creating a customer
# from the core app to the store app.
# The responsibilities are better distributed across various apps.


# this function should be called when a user is saved
# sender is the class sending a notification or a signal
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']: # boolean
        Customer.objects.create(user=kwargs['instance'])


# this function is executed unless import to the apps.py in the config class
# and overwrites the ready method