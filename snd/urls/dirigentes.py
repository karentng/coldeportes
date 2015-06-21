from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.dirigentes import *

"""
Autor: Cristian Leonardo Ríos López
Conjunto de formularios pasados al wizard según el paso actual del wizard
"""

urlpatterns = patterns('snd.views.dirigentes',
    url(r'^listar$', 'listar', name='dirigentes_listar'),
    url(r'^finalizar/(?P<opcion>.+)$', 'finalizar', name='dirigentes_finalizar'),
    url(r'^activar_desactivar/(\d+)$', 'activar_desactivar', name='dirigentes_activar_desactivar'),

    #urls wizard
    url(r'^nuevo/wizard/identificacion$', 'wizard_identificacion_nuevo', name='dirigentes_wizard_identificacion_nuevo'),
    url(r'^nuevo/wizard/identificacion/(\d+)$', 'wizard_identificacion', name='dirigentes_wizard_identificacion'), 
    url(r'^nuevo/wizard/funciones/(\d+)$', 'wizard_funciones', name='dirigentes_wizard_funciones'),

    #urls para eliminar los pasos de los que se pueden registrar muchos en el wizard
    url(r'^eliminar/funcion/(\d+)/(\d+)$', 'eliminar_funcion', name='dirigentes_eliminar_funcion'),
)
