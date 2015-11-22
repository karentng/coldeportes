#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.escenarios',
    url(r'^estrato-escenario$', 'estrato_escenarios', name='reportes_escenarios_estrato'),
    url(r'^tipo-escenario$', 'tipos_escenarios', name='reportes_escenarios_tipos'),
    url(r'^estado-fisico$', 'estado_fisico', name='reportes_escenarios_estado_fisico'),
    url(r'^tipo-superficie$', 'tipo_superficie', name='reportes_escenarios_tipo_superficie'),
    url(r'^division-territorial$', 'division_territorial', name='reportes_escenarios_division_territorial'),
)
