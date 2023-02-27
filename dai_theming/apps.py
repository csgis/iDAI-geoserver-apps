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

        run_setup_hooks()

def run_setup_hooks(*args, **kwargs):
    """
    Run basic setup configuration for the custom_metadata app.
    """

    # Add custom URLs
    from django.conf.urls import include, url
    from geonode.urls import urlpatterns
    urlpatterns.insert(
        0,
        url(f"", include(f"dai-gn-custom-apps.dai_theming.urls")),
    )

    # Add middleware
    middleware = list(settings.MIDDLEWARE)
    middleware = ["dai-gn-custom-apps.dai_theming.middleware.BlockSignupMiddleware"] \
                 + middleware \
                 + ["dai-gn-custom-apps.dai_theming.middleware.CheckUserMiddleware"]
    settings.MIDDLEWARE = tuple(middleware)

