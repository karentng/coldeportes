#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.personal_apoyo',
    url(r'^actividades', 'reporte_actividades_personal', name='reporte_actividades_personal'),
)