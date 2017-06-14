from django.apps import AppConfig


class IntuneConfig(AppConfig):
    name = 'intune'

    def ready(self):
        from . import signals

