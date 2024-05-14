from django.apps import AppConfig


class DaardDatabaseConfig(AppConfig):
    name = 'daard_database'

    def ready(self):
        import daard_database.signals #noqa

        # Add custom URLs
        from daard_database import urls as daard_urls
        from django.conf.urls import include, url
        from geonode.urls import urlpatterns
        urlpatterns.insert(
            0,
            url(f"^daard/", include(daard_urls)),
        )