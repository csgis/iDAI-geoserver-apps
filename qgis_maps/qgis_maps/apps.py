from django.apps import AppConfig
from django.conf import settings
import os

class QgisMapsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qgis_maps'

    def ready(self):
        # inject templates
        settings.TEMPLATES[0]["DIRS"].insert(0, os.path.join(self.path, "templates"))
        # run hooks
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
        url(f"^qgis-maps/", include(f"qgis_maps.urls")),
    )
