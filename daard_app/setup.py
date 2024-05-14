import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='daard_database',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='GPL',
    description='A Django app for DAARD Database.',
    long_description=README,
    url='https://geoserver.dainst.org',
    author='Toni Schönbuchner',
    author_email='toni.schoebuchner@cuprit.net',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 2.2.13',
        'Intended Audience :: Developers',
        'License :: GPL',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=[
        'Django~=3.0',
        'django-admin-select2==1.0.1',
        'django-easy-select2==1.5.8',
        'django-bootstrap-select==0.1.3',
        'django-mptt>=0.14.0',
        'djangorestframework~=3.0',
        'django-filter>=22.0,<24.0',
        'drf-spectacular>=0.25.0,<0.27.0',
        'django-geoposition-2==0.4.0',
        'django-nested-inline==0.4.5',
        'Markdown~=3.0',
        'django-import-export',
        'django-jsonfield'
    ]
)


