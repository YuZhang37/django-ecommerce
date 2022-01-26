from storefront.settings.common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1%1=)3x)36h6#v6ij745g$g@h8xp+x(u@3@5f_8hdlx9)xp_h5'

# when ALLOWED_HOSTS is empty, the project serves hosts against default values
# when specified, only serve the allowed hosts
# just simply match the host in the request against the list
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '0.0.0.0',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'storefront',
        'NAME': 'storefront',
        'HOST': '0.0.0.0',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
    }
}

