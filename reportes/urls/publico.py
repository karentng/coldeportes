#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.publico',
    url(r'^tipos$', 'tipos', name='reportes_publico_tipos'),
    url(r'centros-acondicionamiento/', include('reportes.urls.caf')),
)
