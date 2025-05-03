from django.apps import AppConfig


class GarbagedetectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GarbageDetector'

    def ready(self):
        import GarbageDetector.signals

