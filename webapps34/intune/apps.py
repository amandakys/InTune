from django.apps import AppConfig


class IntuneConfig(AppConfig):
    name = 'intune'

    def ready(self):
        import intune.signals

