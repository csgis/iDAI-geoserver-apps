from django.http import Http404, FileResponse, HttpResponse
from django.views.static import serve
import os
from django.shortcuts import redirect, get_object_or_404
from .models import QGIS_Maps
from guardian.shortcuts import get_perms
from geonode.base.models import ResourceBase
import re
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.conf import settings
import mimetypes

def check_user_perms_on_resource(request, resource_id: int = None, folder_name: str = None):
    qgis_map = None

    if resource_id:
        qgis_map = get_object_or_404(QGIS_Maps, resource=resource_id)
        resource = qgis_map.resource
        if 'view_resourcebase' not in get_perms(request.user, resource):
            raise PermissionDenied("You don't have permission to view this resource.")

    if folder_name:
        folder_name_match = re.findall('[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}', folder_name)
        if folder_name_match:
            folder_name = folder_name_match[0]
            qgis_map = get_object_or_404(QGIS_Maps, folder_name=folder_name)
            resource = qgis_map.resource
            if 'view_resourcebase' not in get_perms(request.user, resource):
                print("no permissions")
                raise PermissionDenied("You don't have permission to view this resource.")
        else:
            # The regex didn't match any folder name
            raise ValueError("Invalid folder name format")

    return qgis_map



def serve_static_file(request, uuid, sub_dir="", filename=None):
    # check if user can view base resource
    check_user_perms_on_resource(request, folder_name=uuid)


    pages_dir = os.path.join(settings.MEDIA_ROOT, "pages", uuid )
    if sub_dir:
        pages_dir = os.path.join(pages_dir, sub_dir)
    fullpath = os.path.join(pages_dir, filename)

    # Get the content type based on the file extension
    content_type, encoding = mimetypes.guess_type(fullpath)

    # Set the content type header explicitly for CSS files
    if content_type == 'text/css':
        content_type = 'text/css; charset=utf-8'

    try:
        with open(fullpath, 'rb') as f:
            response = HttpResponse(f.read(), content_type=content_type)
            return response
    except FileNotFoundError:
        raise Http404("File not found")



def render_button(request, resource_id: int):
    qgis_map = get_object_or_404(QGIS_Maps, resource=resource_id)
    hash = qgis_map.folder_name if qgis_map.folder_name else None

    if hash:
        btn = f"""
            <li>
                <a class="nav-link btn btn-secondary btn-sm"
                style="background-color: yellow; color: #333;" target="_blank"
                href="/uploaded/pages/{hash}/index.html">
                <span>3D VIEW</span>
                </a>
            </li>
        """
        return HttpResponse(btn)

    raise Http404("File not found")