#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.caf',
    url(r'^demografia$', 'demografia', name='reportes_caf_demografia'),
)
