from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.deportistas import *


urlpatterns = patterns('snd.views.deportistas',
    #Urls de Wizard
    url(r'^crear$', 'crear_deportista', name='deporista_nuevo'),
    url(r'^listar$', 'listar_deportista', name='deporista_lista'),
    url(r'^desactivar', 'desactivar_deportista', name='deporista_desactivar'),
    #Urls de eliminacion de muchos en el wizard

    #Urls de listado y desactivacion
)
