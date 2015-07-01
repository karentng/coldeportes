from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.entrenadores import *



urlpatterns = patterns('snd.views.entrenadores',

    #Urls de Wizard
    url(r'^wizard/identificacion$', 'wizard_entrenador_nuevo', name='entrenador_nuevo'),
    url(r'^wizard/identificacion/(\d+)$', 'wizard_entrenador', name='edicion_entrenador'),
    url(r'^wizard/formacion-deportiva/(\d+)$', 'wizard_formacion_deportiva', name='wizard_formacion_deportiva'),
    url(r'^wizard/experiencia-laboral/(\d+)$', 'wizard_experiencia_laboral', name='wizard_experiencia_laboral'),

    #Urls de eliminacion de muchos en el wizard
    url(r'^eliminar/formacion-deportiva/(\d+)/(\d+)$', 'eliminar_formacion_deportiva', name='eliminar_formacion_deportiva'),
    url(r'^eliminar/experiencia-laboral/(\d+)/(\d+)$', 'eliminar_experiencia_laboral', name='eliminar_experiencia_laboral'),

    #Urls de listado y desactivacion
    url(r'^listar$', 'listar_entrenador', name='entrenador_listar'),
    url(r'^desactivar/(\d+)$', 'desactivar_entrenador', name='entrenador_desactivar'),
    url(r'^finalizar', 'finalizar_entrenador', name='finalizar_entrenador'),
    url(r'^ver/(\d+)$','ver_entrenador',name='ver_entrenador'),
)
