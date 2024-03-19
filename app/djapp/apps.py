from django.apps import AppConfig


class DjappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djapp'

    def ready(self):
        from .dispatchers import update_search_vector  # Import and register the signal handlers
