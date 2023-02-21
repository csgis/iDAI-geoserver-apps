from django.apps import AppConfig, apps
from django.conf import settings
import os


class DaiThemingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dai-gn-custom-apps.dai_theming'

    def ready(self):
        # inject templates
        settings.TEMPLATES[0]["DIRS"].insert(0, os.path.join(self.path, "templates"))

        # load signals
        signals_module = f"{self.name}.signals"
        __import__(signals_module)

