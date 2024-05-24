from django.urls import re_path
from custom_metadata.views import (
    metadata_apps_form_view_decorator,
    metadata_apps_detail_view_decorator,
)

urlpatterns = [
    re_path(
        r"^(?P<geoappid>\d+)/metadata$",
        metadata_apps_form_view_decorator,
        name="geoapp_metadata",
    ),
    re_path(
        r"^(?P<geoappid>[^/]*)/metadata_detail$",
        metadata_apps_detail_view_decorator,
        name="geoapp_metadata_detail",
    ),
]
