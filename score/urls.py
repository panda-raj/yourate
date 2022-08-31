from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^get_score/$', views.get_score, name='get_score')
]