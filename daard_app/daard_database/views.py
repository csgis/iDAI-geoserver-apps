from .serializers import DiseaseLibrary, BoneChangeBoneProxySerializer, \
    BoneSerializer, DiseaseCaseSerializer, DiseaseSerializer, BoneChangeFileSerializer
from django.db.models import Q
from .models import DiseaseCase, BoneChangeBoneProxy, Bone, InstitutList, BoneChangeFile
from rest_framework.response import Response
import requests
from rest_framework import status
from .choices import forms
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.views.generic import TemplateView
import logging
logger = logging.getLogger("geonode")
from slugify import slugify

# imports for daard status page
import psycopg2
import os
from daard_database.models import DiseaseCase
from django.conf import settings
from collections import defaultdict
from django.db.models import Prefetch

table_name = os.getenv('DAARD_LAYERNAME',"daard_database")

class BonesImageView(TemplateView):
    template_name = 'daard_bones.html'

class DaardStatus(TemplateView):
    template_name = 'daard_status.html'
    def get_context_data(self, *args, **kwargs):
        context = super(DaardStatus, self).get_context_data(*args, **kwargs)
        connection = psycopg2.connect(
            user=settings.DATABASES['datastore']['NAME'],
            password=settings.DATABASES['datastore']['PASSWORD'],
            host=settings.DATABASES['datastore']['HOST'],
            port=settings.DATABASES['datastore']['PORT'],
            database=settings.DATABASES['datastore']['NAME']
        )
        cursor = connection.cursor()
        all_cases = DiseaseCase.objects.all()

        c = 1
        context['results'] = []
        for case in all_cases:
            q = f"select uuid from {table_name} where uuid='{case.uuid}'"
            cursor.execute(q)
            records = cursor.fetchall()
            found_records = len(records)

            # print(case.uuid)
            siteurl = f'{settings.SITEURL}de/admin/daard_database/diseasecase/{case}/change/'
            case = str(case)
            if (found_records == 0):
                context['results'].append({
                    'counter': c,
                    'id': case,
                    'status': 'BAD',
                    'url': siteurl
                })
            elif (found_records > 0):
                context['results'].append({
                    'counter': c,
                    'id': case,
                    'status': 'GOOD',
                    'url': siteurl
                })
            else:
                context['results'].append({
                    'counter': c,
                    'id': case,
                    'status': 'BAD More than once found',
                    'url': siteurl
                })

            c = c + 1

        q = f"select uuid from {table_name}"
        cursor.execute(q)
        records = cursor.fetchall()
        context['map_records'] = len(records)
        context['disease_records'] = len(all_cases)

        return context

# Disease Case
class DiseaseCaseViewset(viewsets.ModelViewSet):
    serializer_class = DiseaseCaseSerializer
    queryset = DiseaseCase.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=disease']
    http_method_names = ['get', 'post', 'head']
    permission_classes = [IsAuthenticatedOrReadOnly]


class DiseaseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    serializer_class = DiseaseSerializer
    queryset = DiseaseLibrary.objects.all()


    def get_queryset(self):
        queryset = DiseaseLibrary.objects.all()
        search_bones = self.request.query_params.get('bone__name__in')
        search_technics = self.request.query_params.get('technic__name__in')
        search_age = self.request.query_params.get('search_age')

        # Filter by Bone
        # http://localhost:8000/api/disease-search/?bone__name__in=Right%20Ribs,Splanchnocranium
        if search_bones is not None:
            search_bones.strip()
            search_bones = search_bones.split(',')
            q = Q()
            for bone in search_bones:
                q = q | Q(anomalies__bone__name__contains=bone)
            queryset = queryset.filter(q)

        # Filter by Technics
        # http://localhost:8000/api/disease-search/?bone__name__in=Left&technic__name__in=Micro
        if search_technics is not None:
            search_technics.strip()
            search_technics = search_technics.split(',')
            q = Q()
            for technic in search_technics:
                q = q | Q(anomalies__technic__name__contains=technic)
            queryset = queryset.filter(q)

        # Filter by Age
        # http://127.0.0.1:8000/api/disease-search/?search_age=subadults,adults&fields=id,name,adults,subadults
        if search_age is not None:
            search_age.strip()
            search_age = search_age.split(',')

            q = Q()
            for age in search_age:
                term = {age.lower(): True}
                q = q | Q(**term)
            queryset = queryset.filter(q)

        # return the filtered queryset
        return queryset


class BoneChangeBoneProxyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    serializer_class = BoneChangeBoneProxySerializer

    def get_queryset(self):
        queryset = BoneChangeBoneProxy.objects.all()
        search_bone = self.request.query_params.get('bone__id__in')

        # Filter by Bone
        # http://localhost:8000/api/bone-change-to-bones/?bone__id__in=1,2
        if search_bone is not None:
            search_bone = search_bone.rstrip(',')
            search_bone = search_bone.split(',')
            q = Q()
            q = Q(bone__pk__in=search_bone)
            queryset = queryset.filter(q)
        return queryset

    def get_bone(self):
        return


class ChangeSearchViewSet(viewsets.ViewSet):
    def list(self, request):
        q = self.request.query_params.get('q')
        search_bone = self.request.query_params.get('bone_ids')

        if q is None or search_bone is None:
            return Response({'body': '?q=<disease_name>&bone_ids=<1,2,3> needed for search'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not q.isdecimal():
            return Response({})

        search_bone_ids = list(filter(bool, search_bone.split(',')))
        bone_changes = self.get_bone_changes(q, search_bone_ids)
        result = self.format_response(bone_changes, search_bone_ids)

        return Response(result if result else {})

    def get_bone_changes(self, disease_id, bone_ids):
        bone_files_prefetch = Prefetch('bone_change__files', queryset=BoneChangeFile.objects.all())
        return BoneChangeBoneProxy.objects.filter(
            anomalies__id=disease_id,
            bone__id__in=bone_ids
        ).prefetch_related('bone', bone_files_prefetch).distinct()

    def format_response(self, bone_changes, bone_ids):
        all_technics = defaultdict(lambda: defaultdict(lambda: {'options': []}))
        absent_unknown = [{'id': 10000, 'name': 'Absent'}, {'id': 10001, 'name': 'Unknown'}]

        for bc in bone_changes:
            for bone in bc.bone.all():
                if str(bone.id) in bone_ids:
                    tech_name = bc.technic.name if bc.technic else 'Unknown'
                    bone_data = {
                        'id': bone.id,
                        'name': slugify(bone.name),
                        'name_complete': f'{bone.name} ({bone.section})',
                        'section': bone.section
                    }

                    # Create a serializer instance with context
                    file_serializer = BoneChangeFileSerializer(bc.bone_change.files.all(), many=True,
                                                               context={'request': self.request})
                    file_data = [file_info for file_info in file_serializer.data]

                    bone_change_with_files = {
                        'id': bc.bone_change.id,
                        'name': bc.bone_change.name,
                        'files': file_data
                    }

                    all_technics[tech_name][bone.id].update(bone_data)
                    all_technics[tech_name][bone.id]['options'].extend([bone_change_with_files])

        for tech in all_technics:
            for opt in all_technics[tech].values():
                opt["options"].insert(0, {"id": 10001, "name": "Unknown", "files": []})
                opt["options"].insert(0, {"id": 10000, "name": "Absent", "files": []})
                opt["options"].insert(0, {"id": 10002, "name": "Not applied", "files": []})

        return all_technics


class FormularConfig(viewsets.ViewSet):
    def list(self, request):

        # Read Bones from Model
        bones = Bone.objects.filter(parent=None).prefetch_related("options").all()
        bone_serializer = BoneSerializer(bones, many=True)

        instituts = InstitutList.objects.values().order_by('position')

        all_bones = bone_serializer.data
        bone_sections = {}

        for bone in all_bones:
            bone_sections[bone["section"]] = []

        for bone in all_bones:
            bone = dict(bone)
            bone["name_complete"] = f"{bone['name']} ({bone['section']})"
            bone["type"] = "selectfield" if bone["options"] else "Label"
            bone["svgid"] = bone["svgid"] if bone["svgid"] else ""
            bone_sections[bone["section"]].append(bone)

            bone_sections[bone["section"]].append(
                {"name": f"{bone['name']}_amount",
                 "id": bone["id"],
                 "section": bone["section"],
                 "type": "selectfield",
                 "options": [
                     {"name":">75%","value":">75%"},
                     {"name":"<75%","value":"<75%"},
                     {"name":"absent","value":"Absent"},
                     {"name":"unknown","value":"% unknown"}
                 ]
                 })

        # build forms from choices.py
        all_forms = {}
        for step in forms:
            for objects in forms[step]:
                key_values = []

                if "values" in forms[step][objects]:
                    forms[step][objects]['options'] = forms[step][objects].pop("values")
                    forms[step][objects]['options'] = [{"name": i[0], "value": i[1]} for i in forms[step][objects]['options']]
                if step != "general":
                    all_forms[step] = forms[step]

        # all_forms["inventory"] = all_bones
        all_forms["inventory"] = bone_sections

        # Set storage place values
        institut_dict = []
        for institut in instituts:
            institut_dict.append({"name": institut['name'], "value": institut['name']})

        all_forms["site"]["storage_place"]["options"] = institut_dict

        # allow reduction of output based on key
        filter_by_key = self.request.query_params.get('filter_by_key')
        if filter_by_key is not None:
            all_forms = all_forms.get(filter_by_key)

        return Response(
            all_forms
            # + all_bones
        )


class SiteServiceAPI(viewsets.ViewSet):
    def list(self, request):
        q = self.request.query_params.get('q')
        task = self.request.query_params.get('task')

        if q is None or task is None:
            return Response({'body': '?q=<term> needed for search; &task=<suggestion|site> needed for search'},
                            status=status.HTTP_400_BAD_REQUEST)

        if task != "site":
            external_api_response = requests.get(f'https://gazetteer.dainst.org/suggestions?field=nameSuggestions&queryId=2&lang=en&text={q}')
        else:
            external_api_response = requests.get(
                f'https://gazetteer.dainst.org/search.json?q={q}&fq=_exists_:prefLocation.'
                f'coordinates&limit=1&type=&pretty=true')

        external_api_response_json = external_api_response.json()
        if task == "site":
            if not external_api_response_json["result"]:
                return Response(external_api_response_json, status=external_api_response.status_code)

            site = external_api_response_json["result"][0]
            prefName = site["prefName"]

            # set preName to english if present
            if "name" in site.keys():
                all_names_in_langauges = {c_lang["language"]: (c_lang) for c_lang in site["names"]}
                if "eng" in all_names_in_langauges:
                    prefName = all_names_in_langauges["eng"]
                else:
                    prefName = site["prefName"]

            return_arr = {"values": []}
            return_arr["values"].append({
                "site": prefName,
                "names": site["names"] if "names" in site.keys() else [],
                "position": site["prefLocation"]["coordinates"],
                "gazId": site["gazId"],
                "gaz_link": site["@id"],
                "types": site["types"]
            })

            external_api_response_json = return_arr

        return Response(external_api_response_json, status=external_api_response.status_code)


class ChronologyServiceAPI(viewsets.ViewSet):
    def list(self, request):
        q = self.request.query_params.get('q')

        if q is None:
            return Response({'body': '?q=<term> needed for search'}, status=status.HTTP_400_BAD_REQUEST)
        return_arr = {"values": set()}
        #external_api_response = requests.get(f'https://chronontology.dainst.org/data/period?q={q}&size=500')
        # f'&q={q}%20AND%20!(_exists_:resource.relations.isPartOf)' \
        base_url = "https://chronontology.dainst.org/data/period/"
        chrono_query =  f'?facet=resource.provenance' \
                        f'&facet=resource.types' \
                        f'&facet=regions.de' \
                        f'&fq=resource.types%3A"material_culture"' \
                        f'&fq=resource.provenance%3A"Chronontology"' \
                        f'&q={q}' \
                        f'&from=0&size=100'
        external_api_response = requests.get(base_url+chrono_query)
        external_api_response_json = external_api_response.json()
        for res in external_api_response_json["results"]:
            first_region = ""
            if "regions" in res:
                if (len(res["regions"]) > 0):
                    first_region = res["regions"][0].get("en","")
                    first_region = f" ({first_region})" if first_region else ""
            if "en" in res["resource"]["names"]:
                english_terms = res["resource"]["names"]["en"][0] + first_region
                return_arr["values"].add(english_terms)
        return_arr["values"] = sorted(return_arr["values"])
        return Response(return_arr, status=external_api_response.status_code)
