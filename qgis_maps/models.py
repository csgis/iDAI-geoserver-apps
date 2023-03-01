import os
import shutil
import uuid
import zipfile
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from geonode.base.models import ResourceBase
import re

def get_pages_upload_path(instance, filename):
    """Returns the relative path to the pages directory."""
    return os.path.join('pages', str(uuid.uuid4()))


class QGIS_MapsManager(models.Manager):
    def delete(self, *args, **kwargs):
        for obj in self.get_queryset().all():
            obj.delete(*args, **kwargs)


class QGIS_Maps(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    resource = models.OneToOneField(ResourceBase, on_delete=models.CASCADE)
    zip_file = models.FileField(upload_to=get_pages_upload_path)
    folder_name = models.CharField(max_length=255, blank=True)
    directory_path = models.CharField(max_length=500, blank=True, null=True)

    objects = QGIS_MapsManager()

    class Meta:
        verbose_name = _("QGIS Map")
        verbose_name_plural = _("Add QGIS Map")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Create a unique folder name within the pages directory
        folder_name = str(uuid.uuid4())
        extract_path = os.path.join(settings.MEDIA_ROOT, "pages", folder_name)

        # Unzip all files from the uploaded zip into the created directory
        zip_ref = zipfile.ZipFile(self.zip_file.path, 'r')
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)
        zip_ref.extractall(extract_path)
        zip_ref.close()

        # Save the full path to the extracted directory
        self.directory_path = extract_path
        self.folder_name = folder_name

        # Update the paths in index.html
        index_file_path = os.path.join(extract_path, 'index.html')
        with open(index_file_path, 'r') as f:
            content = f.read()
        content = re.sub(r'<script src="\.\/(.*?)"><\/script>', f'<script src="/uploaded/pages/{folder_name}/\\1"></script>', content)
        content = content.replace('app.loadSceneFile("./data/Start/scene.js", function (scene) {', f'app.loadSceneFile("/uploaded/pages/{folder_name}/data/Start/scene.js", function (scene) {{')
        content = content.replace('<script type="text/javascript" src="js/',
                                  f'<script type="text/javascript" src="/uploaded/pages/{folder_name}/js/')
        content = content.replace('"models/',
                                  f'"/uploaded/pages/{folder_name}/models/')
        content = content.replace('"skins/',
                                  f'"/uploaded/pages/{folder_name}/skins/')

        with open(index_file_path, 'w') as f:
            f.write(content)

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        ret = super(QGIS_Maps, self).delete(*args, **kwargs)

        # Delete the extracted directory and the zip file from the pages directory
        dir_path = os.path.join(settings.MEDIA_ROOT, self.directory_path)
        try:
            shutil.rmtree(dir_path)
        except Exception as e:
            print(f"Error deleting directory {dir_path}: {e}")
        try:
            os.remove(self.zip_file.path)
        except Exception as e:
            print(f"Error deleting file {self.zip_file.path}: {e}")

        return ret
