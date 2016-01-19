#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.escenarios',
    url(r'^caracteristicas-escenarios$', 'caracteristicas_escenarios', name='reportes_caracteristicas_escenarios'),

    url(r'^periodicidad-mantenimiento$', 'periodicidad_mantenimiento', name='reportes_escenarios_periodicidad_mantenimiento'),
    
    url(r'^disponibilidad-escenario$', 'disponibilidad_escenarios', name='reportes_disponibilidad_escenarios'),

    url(r'^comunas-escenarios$', 'comunas_escenarios', name='reportes_escenarios_comunas'),
    
    url(r'^clase-escenarios$', 'clase_escenarios', name='reportes_clase_escenarios'),

    url(r'^cantidad-espectadores','cantidad_espectadores',name='reporte_cantidad_espectadores')
)
