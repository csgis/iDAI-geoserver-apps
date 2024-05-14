
import os

layername = os.getenv('DAARD_LAYERNAME', "daard_database")

update_sql = f"UPDATE public.{layername} " \
             "SET the_geom=ST_MakePoint(%s, %s), is_approved=%s, \"owner\"=%s, uuid=%s, " \
             "adults=%s, subadults=%s, disease=%s, age_class=%s, age_freetext=%s, " \
             "sex=%s, sex_freetext=%s, bone_relations=%s, reference_images=%s, origin=%s, " \
             "site=%s, gazid=%s, gaz_link=%s, archaeological_tombid=%s, " \
             "archaeological_individualid=%s, archaeological_funery_context=%s, " \
             "archaeological_burial_type=%s, storage_place=%s, storage_place_freetext=%s, " \
             "chronology=%s, age_estimation_method=%s,chronology_freetext=%s, dating_method=%s, size_from=%s, " \
             "size_to=%s, size_freetext=%s, dna_analyses=%s, dna_analyses_link=%s, published=%s, " \
             "doi=%s, c_bones=%s, c_no_o_bones=%s, c_b_t_bc_rel=%s, c_technic=%s, svgid=%s, " \
             "\"references\"=%s, comment=%s, differential_diagnosis=%s " \
             "WHERE uuid=%s;"


insert_sql = f"INSERT INTO public.{layername} " \
             "(the_geom, is_approved, \"owner\", uuid, adults, subadults, disease, " \
             "age_class, age_freetext, sex, sex_freetext, bone_relations, reference_images, " \
             "origin, site, gazid, gaz_link, archaeological_tombid, archaeological_individualid, " \
             "archaeological_funery_context, archaeological_burial_type, storage_place, " \
             "storage_place_freetext, chronology, age_estimation_method, chronology_freetext, " \
             "dating_method, size_from, size_to, size_freetext, dna_analyses, dna_analyses_link, " \
             "published, doi, c_bones, c_no_o_bones, c_b_t_bc_rel, c_technic, svgid, " \
             "\"references\", comment, differential_diagnosis) " \
             "VALUES " \
             "(ST_MakePoint(%s, %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
             "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
             "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"


sql_delete_str = f"DELETE FROM public.{layername} " \
                 f"WHERE uuid=%s;"