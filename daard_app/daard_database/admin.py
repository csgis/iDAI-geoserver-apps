from django.contrib import admin
from .models import DiseaseCase, DiseaseLibrary, BoneChange, Bone, Technic, BoneChangeBoneProxy, BoneRelation, \
    InstitutList, Helper, DiseaseAlias, BoneChangeFile
from mptt.admin import DraggableMPTTAdmin
from import_export.admin import ImportExportModelAdmin


# the helper proxy registry, will not get registered itself
class BoneChangeBoneProxy(admin.TabularInline):
    model = BoneChangeBoneProxy
    extra = 1
    autocomplete_fields = ['technic', 'bone_change']
    """
    # add the extrascript for turning multiple selects into a checkbox table
    class Media:
        js = ['/static/js/daard_database.js']
    """


class BoneRelation(admin.TabularInline):
    model = BoneRelation
    extra = 1


class DiseaseAliasInline(admin.StackedInline):
    model = DiseaseAlias
    extra = 1
    fields = ['name',]

class DiseaseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = DiseaseLibrary

    inlines = [DiseaseAliasInline, BoneChangeBoneProxy]
    search_fields = ('name',)

    # add the extrascript for turning multiple selects into a checkbox table

    class Media:
        js = ['//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js', '/static/js/checkboxes.js']
        # js = ['//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js']
        css = {
            'all': ('/static/css/checkbox.css',)
        }


# the ordinary models
class TechnicAdmin(admin.ModelAdmin):
    model = Technic
    search_fields = ['name']

class BoneAdmin(ImportExportModelAdmin, DraggableMPTTAdmin):
    model = Bone
    search_fields = ('name',)
    list_filter = ('section',)
    # list_display = ('indented_title', 'section',)
    list_display = ('indented_title',)


class BoneChangeFileInline(admin.TabularInline):
    model = BoneChangeFile
    extra = 1

class BoneChangeAdmin(admin.ModelAdmin):
    model = BoneChange
    inlines = [BoneChangeFileInline]
    search_fields = ['name']


class HelperAdmin(admin.ModelAdmin):
    model = Helper
    search_fields = ['name']

class InstitutListAdmin(admin.ModelAdmin):
    model = InstitutList
    search_fields = ['name']
    list_display = ('name', 'position',)
    ordering = ('position',)

class DiseaseCaseAdmin(admin.ModelAdmin):
    model = DiseaseCase
    list_display = ('disease', 'is_approved', 'site', 'owner', 'uuid', 'date_created', 'date_last_updated')
    readonly_fields = ('date_created', 'date_last_updated')
    search_fields = ['disease']
    # inlines = [BoneRelation]

    class Media:
        js = ['//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js', '/static/js/checkboxes.js']
        # js = ['//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js']
        css = {
            'all': ('/static/css/checkbox.css',)
        }
        """
    fieldsets = (
        ('Specific', {
           'fields': ('disease', 'geoserver_id', 'bone')
        }),
        ('General', {
            'fields': ('adults','subadults','age_class', 'age_freetext','sex','archaeological_site',
                       'archaeological_tombid','archaeological_individualid',
                       'archaeological_funery_context','archaeological_burial_type',
                       'collection_link',
                       'storage_place',
                       'storage_place_freetext',
                       'storage_condition',
                       'chronology',
                       'chronology_freetext',
                       'dating_method','dna_analyses',
                       'dna_analyses_freetext',
                       'publication',
                       'publication_freetext',),
        }),
        ('Contact', {
            'fields': ('contact_firstname','contact_lastname','contact_institut',
                       'contact_email','position',),
        }),
    )
    """


# Register Objects
admin.site.register(Technic, TechnicAdmin)
admin.site.register(Bone, BoneAdmin)
admin.site.register(BoneChange, BoneChangeAdmin)
admin.site.register(Helper, HelperAdmin)
admin.site.register(InstitutList, InstitutListAdmin)
#admin.site.register(DiseaseAlias, DiseaseAliasAdmin)
admin.site.register(DiseaseLibrary, DiseaseAdmin)
# admin.site.register(FormConfig)
admin.site.register(DiseaseCase, DiseaseCaseAdmin)
