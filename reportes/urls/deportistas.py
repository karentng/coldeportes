#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.deportistas',
    url(r'^participaciones$', 'participaciones_deportivas', name='reporte_participaciones_deportivas'),
)
