""" конфигурация приложения Объявления """
from django.apps import AppConfig


class AdvertConfig(AppConfig):
    """ конфигурация приложения Объявления """
    default_auto_field = "django.db.models.BigAutoField"
    name = "advert"
    verbose_name = "Объявления и отклики"

    def ready(self):
        import advert.signals
