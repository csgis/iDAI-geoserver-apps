from django.urls import path
from . import views

urlpatterns = [
    path('howto/', views.howto_view, name='howto'),
]
