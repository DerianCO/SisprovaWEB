from django.conf.urls import url
from API.REST.views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^reporte/$', csrf_exempt(reporte)),
]
