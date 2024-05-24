from django.urls import re_path
from custom_metadata.views import (
    metadata_documents_form_view_decorator,
    metadata_documents_detail_view_decorator,
)

urlpatterns = [
    re_path(
        r"^(?P<docid>\d+)/metadata$",
        metadata_documents_form_view_decorator,
        name="document_metadata",
    ),
    re_path(
        r"^(?P<docid>[^/]*)/metadata_detail$",
        metadata_documents_detail_view_decorator,
        name="document_metadata_detail",
    ),
]
