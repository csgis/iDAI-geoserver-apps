from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from geonode.people.models import Profile
from geonode.base.models import ResourceBase
from geonode.layers.models import Dataset
from geonode.layers.utils import set_datasets_permissions
from guardian.shortcuts import assign_perm
from celery import shared_task
from datetime import timedelta


@receiver(post_save, sender=Profile)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        email = instance.email.lower()
        company_domains = getattr(settings, "COMPANY_EMAIL_DOMAINS", ["csgis.de", "dainst.de",])
        group_name = getattr(settings, "COMPANY_VIEW_PERMISSION_GROUP", "dai-user")

        if any(email.endswith(domain) for domain in company_domains):
            group, created = Group.objects.get_or_create(name=group_name)
            instance.groups.add(group)


@shared_task(queue="security")
def assign_view_permission_for_company_group(instance_name, group_name):
    set_datasets_permissions(
        "view", resources_names=[instance_name], groups_names=[group_name], delete_flag=False, verbose=True
    )
    import sys
    current_name = __name__
    print(f"Current name: {current_name} {timezone.now()}", file=sys.stderr)


@receiver(post_save, sender=Dataset)
def handle_view_permission_for_internal_group(sender, instance, created, **kwargs):
    if created:
        eta = timezone.now() + timedelta(seconds=5)
        group_name = getattr(settings, "COMPANY_VIEW_PERMISSION_GROUP", "dai-user")
        assign_view_permission_for_company_group.apply_async(
            args=(instance.name, group_name,),
            eta=eta,
        )



"""
@receiver(post_save, sender=ResourceBase)
def assign_view_permission_to_dai_internal(sender, instance, created,  **kwargs):
    print("run permissions update")
    print(created)
    if instance.pk or created:
        group = Group.objects.get(name='dai-user')
        if not group.permissions.filter(codename='view_resourcebase').exists():
            print("here")
            assign_perm('view_resourcebase', group, instance)
"""
