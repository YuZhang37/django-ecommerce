# define signals in the __init__ module
from django.dispatch import Signal

order_created = Signal()
# a signal is simply an instance of the Signal class