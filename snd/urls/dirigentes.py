from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.dirigentes import *


urlpatterns = patterns('snd.views.dirigentes',
    url(r'^nuevo$', 'crearDirigente', name='dirigentes_crear'),
    url(r'^listar$', 'listarDirigentes', name='dirigentes_listar'),
)