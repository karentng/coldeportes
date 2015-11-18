#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.caf',
    url(r'^demografia$', 'demografia', name='reportes_caf_demografia'),
    url(r'^generar$', 'generar', name='generar'),

    url(r'^report_caf_publico$', 'report_caf_publico', name='report_caf_publico'),
)
