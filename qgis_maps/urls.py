from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^render-btn/(?P<resource_id>\d+)$', views.render_button),
    re_path(r'^(?P<uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/(?P<sub_dir>.*/)?(?P<filename>.*\.(js|png|css|html|jpg|jpeg))$', views.serve_static_file),

]