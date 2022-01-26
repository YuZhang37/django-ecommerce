from storefront.settings.common import *
import os
import dj_database_url
DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

# when ALLOWED_HOSTS is empty, the project serves hosts against default values
# when specified, only serve the allowed hosts
# just simply match the host in the request against the list

# if debug is false, must set up ALLOWED_HOSTS,
# specify the servers that can run our application
ALLOWED_HOSTS = ['marvinbuy-prod.herokuapp.com']


DATABASES = {
    'default': dj_database_url.config()
    # this function looks for an environment variable called DATABASE_URL
    # it'll read this variable, it will parse the connection string
    # and returns a dictionary that we can use here

}

REDIS_URL = os.environ['REDIS_URL']

CELERY_BROKER_URL = REDIS_URL

# config redis as the caching backend
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # the location of the redis server
        # database 1 has been used as message broker, use 2 as cache
        "LOCATION": REDIS_URL,
        # the data in cache will be time out in 10 mins
        'TIMEOUT': 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']