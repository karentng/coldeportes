from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.dirigentes import *

"""
Autor: Cristian Leonardo Ríos López
"""

urlpatterns = patterns('snd.views.dirigentes',
    url(r'^listar$', 'listar', name='dirigentes_listar'),
    url(r'^verificar$', 'verificar', name='dirigentes_verificar'),
    url(r'^finalizar/(?P<opcion>.+)/(?P<edicion>\d+)$', 'finalizar', name='dirigentes_finalizar'),
    url(r'^activar_desactivar/(\d+)$', 'activar_desactivar', name='dirigentes_activar_desactivar'),
    url(r'^ver/(\d+)/(\d+)$', 'ver', name='dirigentes_ver'),

    #urls wizard
    url(r'^nuevo/wizard/identificacion$', 'wizard_identificacion_nuevo', name='dirigentes_wizard_identificacion_nuevo'),
    url(r'^nuevo/wizard/identificacion/(\d+)$', 'wizard_identificacion', name='dirigentes_wizard_identificacion'), 
    url(r'^nuevo/wizard/cargos/(?P<dirigente_id>\d+)/(?P<edicion>\d+)$', 'wizard_cargos', name='dirigentes_wizard_cargos'),
    url(r'^nuevo/wizard/funciones/(?P<dirigente_id>\d+)/(?P<edicion>\d+)$', 'wizard_funciones', name='dirigentes_wizard_funciones'),
    url(r'^nuevo/wizard/funciones/(?P<dirigente_id>\d+)/(?P<cargo_id>\d+)/(?P<edicion>\d+)$', 'wizard_funciones', name='dirigentes_wizard_funciones'),

    #urls para eliminar los pasos de los que se pueden registrar muchos en el wizard
    url(r'^eliminar/funcion/(\d+)/(\d+)/(\d+)$', 'eliminar_funcion', name='dirigentes_eliminar_funcion'),
    url(r'^eliminar/cargo/(\d+)/(\d+)$', 'eliminar_cargo', name='dirigentes_eliminar_cargo'),

    #urls para manejo de ajax
    url(r'^cargos$', 'cargos_ajax'),
    url(r'^funciones$', 'funciones_ajax'),
)
