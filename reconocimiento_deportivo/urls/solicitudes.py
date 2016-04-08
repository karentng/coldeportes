#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('reconocimiento_deportivo.views.solicitudes',
    #url(r'^cargar-columnas/(\d+)$', 'cargar_columnas', name='cargar_columnas'),
)