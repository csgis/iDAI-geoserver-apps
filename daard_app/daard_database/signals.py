from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import requests
from .models import DiseaseCase
from django.conf import settings
import os
import psycopg2
import logging
from .send_notification import notify_daard_user
from geonode.people.models import Profile
from .helpers import count_bones, get_bone_names, format_bone_relations, get_technics, get_svgids
import json
from .db_query import update_sql, insert_sql, sql_delete_str


# set variables
logger = logging.getLogger("geonode")
layername = os.getenv('DAARD_LAYERNAME', "daard_database")
geodatabase = settings.DATABASES['datastore']['NAME']
geodatabase_user = settings.DATABASES['datastore']['USER']
geodatabase_password = settings.DATABASES['datastore']['PASSWORD']
geodatabase_port = settings.DATABASES['datastore']['PORT']
geodatabase_host = settings.DATABASES['datastore']['HOST']

# get connection string
def get_connection():
    connection = psycopg2.connect(
        host=geodatabase_host,
        database=geodatabase,
        port=geodatabase_port,
        user=geodatabase_user,
        password=geodatabase_password)

    return connection



@receiver(post_save, sender=DiseaseCase)
def add_or_edit_map_feature(sender, instance, created, **kwargs):

    conn = get_connection()
    # add calculated fields
    instance.svgid = get_svgids(instance)
    instance.c_no_o_bones = count_bones(instance)
    instance.c_bones = get_bone_names(instance)
    instance.c_b_t_bc_rel = format_bone_relations(instance)
    instance.c_technic = get_technics(instance)
    instance.disease_name = instance.disease.name
    instance.storage_place_name = ", ".join(instance.storage_place)
    instance.dating_method = ", ".join(instance.dating_method)
    instance.position = str(instance.position.longitude)+" "+str(instance.position.latitude)
    instance.bone_relations = json.dumps(instance.bone_relations)

    x, y = instance.position.split()
    x = float(x)
    y = float(y)

    owner_email = [instance.owner.email, ]

    # Update table
    cur = conn.cursor()
    data = (x,
            y,
            instance.is_approved,
            instance.owner.id,
            instance.uuid,
            instance.adults,
            instance.subadults,
            instance.disease.name,
            instance.age_class,
            instance.age_freetext,
            instance.sex,
            instance.sex_freetext,
            instance.bone_relations,
            instance.reference_images,
            instance.origin,
            instance.site,
            instance.gazId,
            instance.gaz_link,
            instance.archaeological_tombid,
            instance.archaeological_individualid,
            instance.archaeological_funery_context,
            instance.archaeological_burial_type,
            instance.storage_place_name,
            instance.storage_place_freetext,
            instance.chronology,
            instance.age_estimation_method,
            instance.chronology_freetext,
            instance.dating_method,
            instance.size_from,
            instance.size_to,
            instance.size_freetext,
            instance.dna_analyses,
            instance.dna_analyses_link,
            instance.published,
            instance.doi,
            instance.c_bones,
            instance.c_no_o_bones,
            instance.c_b_t_bc_rel,
            instance.c_technic,
            instance.svgid,
            instance.references,
            instance.comment,
            instance.differential_diagnosis,
            )


    sql_string = insert_sql if created else update_sql

    if not created:
        data = data + (str(instance.uuid),)
        print(data)
    print("Number of placeholders in SQL:", sql_string.count("%s"))
    print("Number of elements in data tuple:", len(data))
    cur.execute(sql_string, data)
    conn.commit()
    cur.close()

    if created:
        if settings.EMAIL_ENABLE:
            # Email notification
            # daard_all_editor__profiles = Profile.objects.filter(groups__name="daard_editors")
            editor_recipients = os.getenv('DAARD_EDITORS', ["toni.schoenbuchner@csgis.de",])
            editor_recipients = editor_recipients.split(',')
            logger.info(editor_recipients)
            #editor_recipients = list(i for i in daard_all_editor__profiles.values_list('email', flat=True) if bool(i))
            notify_daard_user(receiver=editor_recipients,
                              template='./email/admin_notice_created.txt',
                              instance=instance,
                              title='A new entry has been created')

            notify_daard_user(receiver=owner_email,
                              template='./email/user_notice_created.txt',
                              instance=instance,
                              title='Your DAARD Database entry')
    else:
        if settings.EMAIL_ENABLE:
            if instance.is_approved:
                daard_all_editor__profiles = os.getenv('DAARD_EDITORS', ["toni.schoenbuchner@csgis.de"])
                logger.info(daard_all_editor__profiles)
                logger.info(owner_email)

                notify_daard_user(receiver=owner_email,
                                  template='./email/user_resource_published.txt',
                                  instance=instance,
                                  title='Your entry has changed')

    conn.close()

@receiver(post_delete, sender=DiseaseCase)
def delete_map_feature(sender,instance,**kwargs):
        # Delete Item from Map
        conn_delete = get_connection()
        cur = conn_delete.cursor()
        cur.execute(sql_delete_str, (str(instance.uuid),))
        cur.close()
        conn_delete.commit()
        conn_delete.close()

        # Email notification
        receivers = [instance.owner.email, ]
        notify_daard_user(receiver=receivers,
                          template='./email/user_resource_deleted.txt',
                          instance=instance,
                          title='Your entry has been deleted')
