from storefront.settings.common import *
import os

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

# when ALLOWED_HOSTS is empty, the project serves hosts against default values
# when specified, only serve the allowed hosts
# just simply match the host in the request against the list

# if debug is false, must set up ALLOWED_HOSTS,
# specify the servers that can run our application
# TODO allowed hosts with the server
ALLOWED_HOSTS = []

# TODO configure the database
