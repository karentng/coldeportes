#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.caf import *
from snd.formularios.caf  import *
from coldeportes.utilities import all_permission_required

urlpatterns = patterns('snd.views.cargado_datos',
    url(r'^cargar-columnas/(\d+)$', 'cargar_columnas', name='cargar_columnas'),
    url(r'^cargar-datos/(\d+)$', 'cargar_datos', name='cargar_datos'),   
)