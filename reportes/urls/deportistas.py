#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.deportistas',
    url(r'^participaciones$', 'participaciones_deportivas', name='reporte_participaciones_deportivas'),
    url(r'^beneficiario-programa-apoyo', 'beneficiario_programa_apoyo', name='reporte_beneficiario_programa_apoyo'),
    url(r'^usa-centros-biomedicos', 'reporte_uso_centros_biomedicos', name='reporte_uso_centros_biomedicos'),
    url(r'^etnias', 'etinias_deportistas', name='reporte_etinias_deportistas'),
    url(r'^formacion-academica', 'formacion_academica', name='reporte_formacion_academica'),
    url(r'^lgtbi', 'reporte_lgtbi', name='reporte_lgtbi_deportistas'),
    url(r'^doping', 'reporte_doping', name='reporte_doping'),
    url(r'^cantidad-total-deportistas', 'reporte_cantidad_total_deportistas', name='reporte_cantidad_total_deportistas'),
    url(r'^lesiones', 'lesiones_deportivas', name='reporte_lesiones'),
    url(r'^nacionalidad-extranjeros', 'extranjeros_vs_nacionalidad', name='reporte_nacional_extranjero'),
    url(r'^edad','edad_deportistas',name='reporte_edad_deportistas')

)
