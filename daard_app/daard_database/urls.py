
from django.contrib import admin
from django.urls import path, include
from daard_database import views
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

daard_router = DefaultRouter()
daard_router.register('disease-search', views.DiseaseViewSet, basename='disease')
daard_router.register('disease-case', views.DiseaseCaseViewset, basename='disease-case')
daard_router.register('forms', views.FormularConfig, basename='forms')
daard_router.register('gazetteer-sites', views.SiteServiceAPI, basename='sites')
daard_router.register('chronology-periods', views.ChronologyServiceAPI, basename='chronology')
daard_router.register('bone-change-to-bones', views.BoneChangeBoneProxyViewSet, basename='bone-change-to-bones')
daard_router.register('bone-change-search', views.ChangeSearchViewSet, basename='change-search')


urlpatterns = [
    path('api/', include(daard_router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path(r'boneimage', views.BonesImageView.as_view()),
    path(r'status', views.DaardStatus.as_view()),
]

