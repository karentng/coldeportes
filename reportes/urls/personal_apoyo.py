#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.personal_apoyo',
    url(r'^actividades', 'reporte_actividades_personal', name='reporte_actividades_personal'),
    url(r'^formacion-academica', 'reporte_formacion_academica_personal', name='reporte_formacion_academica_personal'),
    url(r'^lgtbi', 'reporte_lgtbi', name='reporte_lgtbi_personal_apoyo'),
    url(r'^cantidad-total-personal-apoyo', 'reporte_cantidad_total_personal_apoyo', name='reporte_cantidad_total_personal_apoyo'),
    url(r'^etnias', 'reporte_etnias', name='reporte_etnias_personal_apoyo'),
    url(r'^nacionalidad', 'reportes_nacionalidad_personal_apoyo', name='reportes_nacionalidad_personal_apoyo'),
)