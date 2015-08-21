from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.cajas_compensacion import *


urlpatterns = patterns('snd.views.cajas_compensacion',
    #urls tabla interactiva
    url(r'^listar$', 'listar_ccfs', name='listar_ccfs'), 
    url(r'^desactivar/(\d+)$', 'desactivar_ccf', name='desactivar_ccf'),
    url(r'^ver/(\d+)$', 'ver_ccf', name='ver_ccf'),
    url(r'^finalizar/(?P<opcion>.+)', 'finalizar_ccf', name='finalizar_ccf'),


    #urls wizard
    url(r'^wizard/nuevo$', 'wizard_caja', name='wizard_caja'), 
    url(r'^wizard/editar/(\d+)$', 'wizard_editar_caja', name='wizard_editar_caja'), 
    url(r'^wizard/horarios/(\d+)$', 'wizard_horarios_ccf', name='wizard_horarios_ccf'), 
    url(r'^wizard/tarifas/(\d+)$', 'wizard_tarifas_ccf', name='wizard_tarifas_ccf'),  
    
    #urls para eliminar los pasos de los que se pueden registrar muchos en el wizard
    url(r'^eliminar/horario/(\d+)/(\d+)$', 'eliminar_horario_ccf', name='eliminar_horario_ccf'),
    url(r'^eliminar/tarifa/(\d+)/(\d+)$', 'eliminar_tarifa_ccf', name='eliminar_tarifa_ccf'), 
)