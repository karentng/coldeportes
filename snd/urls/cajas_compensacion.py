from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.cajas_compensacion import *


urlpatterns = patterns('snd.views.cajas_compensacion',
    #urls tabla interactiva
    url(r'^listar$', 'listar_escenarios_ccfs', name='listar_escenarios_ccfs'), 
    url(r'^desactivar/(\d+)$', 'desactivar_escenario_ccf', name='desactivar_escenario_ccf'),
    url(r'^ver/(\d+)$', 'ver_escenario_ccf', name='ver_escenario_ccf'),
    url(r'^finalizar', 'finalizar_escenario_ccf', name='finalizar_escenario_ccf'),


    #urls wizard
    url(r'^wizard/nuevo$', 'wizard_caja_escenario', name='wizard_caja_escenario'), 
    url(r'^wizard/editar/escenario/(\d+)$', 'wizard_editar_caja_escenario', name='wizard_editar_caja_escenario'), 
    url(r'^wizard/horarios/(\d+)$', 'wizard_horarios_ccf', name='wizard_horarios_ccf'), 
    url(r'^wizard/tarifas/(\d+)$', 'wizard_tarifas_ccf', name='wizard_tarifas_ccf'), 
    url(r'^wizard/contactos/(\d+)$', 'wizard_contactos_ccf', name='wizard_contactos_ccf'), 
    
    #urls para eliminar los pasos de los que se pueden registrar muchos en el wizard
    url(r'^eliminar/horario/(\d+)/(\d+)$', 'eliminar_horario_ccf', name='eliminar_horario_ccf'),
    url(r'^eliminar/tarifa/(\d+)/(\d+)$', 'eliminar_tarifa_ccf', name='eliminar_tarifa_ccf'),
    url(r'^eliminar/contacto/(\d+)/(\d+)$', 'eliminar_contacto_ccf', name='eliminar_contacto_ccf'), 
)