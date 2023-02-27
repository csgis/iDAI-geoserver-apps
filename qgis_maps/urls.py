from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^render-btn/(?P<resource_id>\d+)$', views.render_button),
    re_path(r'^(?P<sub_dir>.+)/(?P<path>.+\.(html|js|css|jpg|png))$', views.serve_static_file),

]