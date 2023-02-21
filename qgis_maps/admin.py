from django.contrib import admin
from .models import QGIS_Maps

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

admin.site.register(QGIS_Maps, QGISMapsAdmin)
