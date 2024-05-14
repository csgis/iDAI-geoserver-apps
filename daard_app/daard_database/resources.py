from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from .models import Bones

class BonesResource(resources.ModelResource):

    name = fields.Field(column_name='name', attribute='name')
    parent = fields.Field(column_name='parent',attribute='parent',widget=ForeignKeyWidget(Bones,'name'))
    parent_id = fields.Field(column_name='parent', attribute='parent', widget=ForeignKeyWidget(Bones, 'id'))

    class Meta:
        model = Bones
        skip_unchanged = True
        report_skipped = False
        fields = '__all__'