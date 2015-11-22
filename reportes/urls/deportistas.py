#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.deportistas',
    url(r'^participaciones$', 'participaciones_deportivas', name='reporte_participaciones_deportivas'),
    url(r'^beneficiario-programa-apoyo', 'beneficiario_programa_apoyo', name='reporte_beneficiario_programa_apoyo'),
    url(r'^etnias', 'etinias_deportistas', name='reporte_etinias_deportistas'),
    url(r'^formacion-academica', 'formacion_academica', name='reporte_formacion_academica'),
    url(r'^nacionalidad', 'nacionalidad', name='reporte_nacionalidad'),
)
