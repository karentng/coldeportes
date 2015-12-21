#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.personal_apoyo',
    url(r'^actividades', 'reporte_actividades_personal', name='reporte_actividades_personal'),
    url(r'^formacion-academica', 'reporte_formacion_academica_personal', name='reporte_formacion_academica_personal'),
    url(r'^lgtbi', 'reporte_lgtbi', name='reporte_lgtbi_personal_apoyo'),
)