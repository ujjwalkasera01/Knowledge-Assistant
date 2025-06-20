from django.apps import AppConfig
import os


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

    def ready(self):
        from .utils.loader import autoload_pdfs

        # Avoid loading during migrations or management commands
        if os.environ.get('RUN_MAIN', None) != 'true':
            return

        print("[Startup] Running autoload_pdfs...")
        autoload_pdfs(upload_dir="media/uploads")  # or wherever your PDFs are
