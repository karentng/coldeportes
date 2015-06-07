from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.deportistas import *


urlpatterns = patterns('snd.views.deportistas',
    #Urls de Wizard
    url(r'^wizard/identificacion$', 'wizard_deportista_nuevo', name='deporista_nuevo'),
    url(r'^wizard/identificacion/(\d+)$', 'wizard_deportista', name='edicion_deportista'),
    url(r'^wizard/composicion-corporal/(\d+)$', 'wizard_corporal', name='wizard_corporal'),

    #Urls de eliminacion de muchos en el wizard

    #Urls de listado y desactivacion
    #url(r'^crear$', 'crear_deportista', name='deporista_nuevo'),
    url(r'^listar$', 'listar_deportista', name='deporista_listar'),
    url(r'^desactivar', 'desactivar_deportista', name='deporista_desactivar'),
)
