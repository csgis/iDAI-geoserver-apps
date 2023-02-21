import os
from django.db import models
from geonode.base.models import ResourceBase
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

APP_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))
PAGES_DIR = os.path.join(APP_DIR, 'pages')

class QGIS_MapsManager(models.Manager):
    def delete(self, *args, **kwargs):
        for obj in self.get_queryset().all():
            obj.delete(*args, **kwargs)

class QGIS_Maps(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    resource = models.OneToOneField(ResourceBase, on_delete=models.CASCADE)
    zip_file = models.FileField(upload_to='pages/')
    folder_name = models.CharField(max_length=255, blank=True)
    directory_path = models.CharField(max_length=500, blank=True, null=True)

    objects = QGIS_MapsManager()

    class Meta:
        verbose_name = _("QGIS Map")
        verbose_name_plural = _("Add QGIS Map")

    def save(self, *args, **kwargs):
        import zipfile
        import os
        import uuid

        super().save(*args, **kwargs)

        # Create a unique folder name within the pages directory
        folder_name = str(uuid.uuid4())
        extract_path = os.path.join(PAGES_DIR, folder_name)

        # Unzip all files from the uploaded zip into the created directory
        zip_ref = zipfile.ZipFile(self.zip_file.path, 'r')
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)
        zip_ref.extractall(extract_path)
        zip_ref.close()

        # Save the full path to the extracted directory
        self.directory_path = extract_path
        self.folder_name = folder_name
        super().save(*args, **kwargs)
        print("save")

    def delete(self, *args, **kwargs):
        ret = super(QGIS_Maps, self).delete(*args, **kwargs)
        import os
        import shutil

        # Delete the extracted directory and the zip file from the pages directory
        dir_path = os.path.join(PAGES_DIR, self.directory_path)
        try:
            shutil.rmtree(dir_path)
        except Exception as e:
            print(f"Error deleting directory {dir_path}: {e}")
        try:
            os.remove(self.zip_file.path)
        except Exception as e:
            print(f"Error deleting file {self.zip_file.path}: {e}")

        return ret
