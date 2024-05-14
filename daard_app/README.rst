=====
DAARD
=====

Daard is a Django app to build a Bone - Disease database.
The Modul will update a geoserver map which acts as an entrypoint.
A decoupled frontend will add user capabilities.

Quick start
-----------

1. Add "daard_database" to your INSTALLED_APPS setting like this::

    GEOPOSITION_BACKEND = 'leaflet'
    GEOPOSITION_MAP_OPTIONS = {
        'minZoom': 3,
        'maxZoom': 15,
    }

    INSTALLED_APPS += (
        'easy_select2',
        'daard_database',
        'geoposition',
        'import_export',
    )

2. The app includes its urls under /daard/api

3. Run ``python manage.py migrate`` to create the daard_database models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Visit http://127.0.0.1:8000/api/daard/ to visit the api

# load initial data

```
./manage.py loaddata /usr/src/daard-database/fixtures/Bone.json
```
