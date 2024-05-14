from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from .choices import forms
from geoposition.fields import GeopositionField
import uuid
from jsonfield import JSONField
from django.conf import settings
from .storage import OverwriteStorage


class Helper(models.Model):
    title = models.CharField(max_length=80)
    pdf = models.FileField(upload_to='pdfs/', help_text="Name must be daard_help.pdf",
                           storage=OverwriteStorage())

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title}"

class DiseaseLibrary(models.Model):
    name = models.CharField(max_length=255)
    subadults = models.BooleanField(default=False, blank=True)
    adults = models.BooleanField(default=False, blank=True)
    
    def __str__(self):
        return self.name

class DiseaseAlias(models.Model):
    name = models.CharField(max_length=600)
    disease = models.ForeignKey(DiseaseLibrary, blank=True, null=True, related_name='aliases', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Technic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class BoneChange(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class BoneChangeFile(models.Model):
    bone_change = models.ForeignKey(BoneChange, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='bone_change_images/')

    def __str__(self):
        return f"File for {self.bone_change.name}"

class InstitutList(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=5)

    def __str__(self):
        return self.name

class Bone(MPTTModel):
    sections = (('cranial_district', 'Cranial district'),
                ('axial_skeleton', 'Axial skeleton'),
                ('right_upper_limb', 'Right upper limb'),
                ('left_upper_limb', 'Left upper limb'),
                ('right_lower_limb', 'Right lower limb'),
                ('left_lower_limb', 'Left lower limb'))
    section = models.CharField(max_length=255, choices=sections)
    name = models.CharField(max_length=255)
    svgid = models.CharField(max_length=255, null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='options', db_index=True,
                            on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        choice = dict(self.sections)
        return f'{self.name} ({choice[self.section]})'


class BoneChangeBoneProxy(models.Model):
    anomalies = models.ForeignKey('DiseaseLibrary', on_delete=models.CASCADE, related_name='anomalies')
    technic = models.ForeignKey('Technic', on_delete=models.CASCADE, related_name='technic_proxy')
    bone_change = models.ForeignKey('BoneChange', blank=True, null=True, on_delete=models.CASCADE, related_name='bone_change_proxy')
    bone = TreeManyToManyField('Bone', related_name='bone_proxy')


class BoneRelation(models.Model):
    anomalies_case = models.ForeignKey('DiseaseCase', on_delete=models.CASCADE, related_name='anomalies_case')
    technic_case = models.ForeignKey('Technic', on_delete=models.CASCADE, related_name='technic_proxy_case')
    bone_change_case = models.ForeignKey('BoneChange', blank=True, null=True, on_delete=models.CASCADE, related_name='bone_change_proxy_case')
    bone_case = TreeManyToManyField('Bone', related_name='bone_proxy_case')


class DiseaseCase(models.Model):
    # commons
    is_approved = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='daard_case_user',
        on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, blank=True)

    # step 1
    adults = models.BooleanField(default=False)
    subadults = models.BooleanField(default=False)
    disease = models.ForeignKey('DiseaseLibrary', on_delete=models.CASCADE, related_name='anomalies_case')
    age_class = models.CharField(max_length=200, choices=forms['disease']['age_class']['values'])
    age_freetext = models.CharField(max_length=200, blank=True, help_text='Narrower age class freetext')
    age_estimation_method = models.CharField(max_length=400, blank=True, help_text='Used method age')

    sex = models.CharField(max_length=200, choices=forms['disease']['sex']['values'])
    sex_freetext = models.CharField(max_length=400, blank=True, null=True, help_text='Method used for sex determination')
    size_from = models.FloatField(null=True, blank=True, help_text="Body size in cm (e.g., 177.10)")
    size_to = models.FloatField(null=True, blank=True, help_text="Body size in cm (e.g., 181.10)")
    size_freetext = models.CharField(max_length=400, blank=True, null=True, help_text='Used method size')

    # step 2
    inventory = JSONField()

    # step 3
    bone_relations = JSONField()

    # step 4
    reference_images = models.CharField(max_length=600, blank=True, null=True)
    origin = models.CharField(max_length=400)
    site = models.CharField(max_length=800, blank=True, null=True)
    gazId = models.CharField(max_length=200, blank=True, null=True, help_text='NOT IN USE ANYMORE')
    gaz_link = models.CharField(max_length=400, blank=True, null=True, help_text='NOT IN USE ANYMORE')

    archaeological_tombid = models.CharField(max_length=400, blank=True, null=True)
    archaeological_individualid = models.CharField(max_length=400, blank=True, null=True)
    archaeological_funery_context = models.CharField(max_length=400, blank=True, null=True, choices=forms['site']['archaeological_funery_context']['values'])
    archaeological_burial_type = models.CharField(max_length=400, blank=True, null=True, choices=forms['site']['archaeological_burial_type']['values'])
    storage_place = JSONField(default=list, blank=True, null=True)
    storage_place_freetext = models.CharField(max_length=400, blank=True, null=True)
    chronology = models.CharField(max_length=400, blank=True, null=True)
    chronology_freetext = models.CharField(max_length=400, blank=True)

    dating_method = JSONField(default=list, blank=True, null=True)




    # step 5
    dna_analyses = models.CharField(max_length=400, choices=forms['publication']['dna_analyses']['values'])
    dna_analyses_link = models.CharField(max_length=400, blank=True, null=True)

    published = models.BooleanField(default=False)
    doi = models.CharField(max_length=400, blank=True, null=True)
    references = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    differential_diagnosis = models.TextField(blank=True, null=True)

    # position
    position = GeopositionField(null=False, blank=True)

    def __str__(self):
        return str(self.id)
