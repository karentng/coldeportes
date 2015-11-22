#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.caf',
    url(r'^ubicación$', 'demografia', name='reportes_caf_demografia'),
    url(r'^estratos$', 'estratos', name='reportes_caf_estratos'),
    url(r'^clases$', 'clases', name='reportes_caf_clases'),
    url(r'^tipos-servicios$', 'tipos_servicios', name='reportes_caf_tipos_servicios'),
)