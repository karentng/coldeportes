#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.escenarios',
    url(r'^estrato$', 'estrato', name='reportes_escenarios_estrato'),
    url(r'^tipo-escenario$', 'tipos_escenarios', name='reportes_escenarios_tipos'),
)
