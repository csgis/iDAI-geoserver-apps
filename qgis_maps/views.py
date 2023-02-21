from django.http import Http404, FileResponse
from django.views.static import serve
import os
from django.shortcuts import redirect, get_object_or_404
from .models import QGIS_Maps
from guardian.shortcuts import get_perms
from geonode.base.models import ResourceBase
import re
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied

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



def serve_static_file(request, path: str):

    # check if user can view base resource
    check_user_perms_on_resource(request, folder_name=path)

    app_dir = os.path.dirname(os.path.realpath(__file__))
    pages_dir = os.path.join(app_dir, "pages")
    try:
        return serve(request, path, document_root=pages_dir)
    except:
        raise Http404("File not found")


def render_button(request, resource_id: int):
    qgis_map = get_object_or_404(QGIS_Maps, resource=resource_id)
    hash = qgis_map.folder_name if qgis_map.folder_name else None

    if hash:
        btn = f"""
            <li>
                <a class="nav-link btn btn-secondary btn-sm"
                style="background-color: white;" target="_blank"
                href="/qgis-maps/{hash}/index.html">
                <span>3D VIEW</span>
                </a>
            </li>
        """
        return HttpResponse(btn)

    raise Http404("File not found")