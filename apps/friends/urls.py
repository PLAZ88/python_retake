from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^/(?P<id>\d+)', views.feature),
    url(r'^/process', views.process),
    url(r'^/remove/(?P<id>\d+)', views.remove)
]

