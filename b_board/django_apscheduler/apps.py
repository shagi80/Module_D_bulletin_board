"""конфигурирования приложения"""
from django.apps import AppConfig


class django_apschedulerConfig(AppConfig):
    """класс Config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_apscheduler'
    verbose_name = "Задачи приложения"