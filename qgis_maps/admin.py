from django.contrib import admin
from .models import QGIS_Maps
from geonode.base.models import ResourceBase


class QGISMapsAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource', 'directory_path', 'zip_file', 'created_at', 'resource_id')
    ordering = ('-created_at',)
    search_fields = ['resource__title', 'title']

    def resource_id(self, obj):
        return obj.resource.id
    resource_id.short_description = 'Resource ID'

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "resource":
            kwargs["queryset"] = ResourceBase.objects.order_by('title')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(QGIS_Maps, QGISMapsAdmin)
