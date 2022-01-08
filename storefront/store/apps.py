from django.apps import AppConfig
# https://dev.to/weplayinternet/upgrading-to-django-3-2-and-fixing-defaultautofield-warnings-518n


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
