#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.publico',
    url(r'^tipos$', 'tipos', name='reportes_publico_tipos'),
    #url(r'caf/', include('reportes.urls.caf')),
    url(r'^bubble$', 'ejemploBubble', name="ejemplo_bubble"),
    url(r'^motion$', 'ejemploMotion', name="ejemplo_motion")
)
