from django.apps import AppConfig


class DjappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djapp'

    # Import and register the signal handlers
    def ready(self):
        from .dispatchers import update_search_vector  
