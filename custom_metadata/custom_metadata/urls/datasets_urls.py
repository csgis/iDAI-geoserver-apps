from django.urls import re_path
from custom_metadata.views import (
    metadata_dataset_form_view_decorator,
    metadata_dataset_detail_view_decorator,
)

urlpatterns = [
    re_path(
        r"^(?P<layername>[^/]*)/metadata$",
        metadata_dataset_form_view_decorator,
        name="dataset_metadata",
    ),
    re_path(
        r"^(?P<layername>[^/]*)/metadata_detail$",
        metadata_dataset_detail_view_decorator,
        name="dataset_metadata_detail",
    ),
]
