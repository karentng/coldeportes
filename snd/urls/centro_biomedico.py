from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.centro_biomedico import *

"""
Autor: Cristian Leonardo Ríos López
"""

urlpatterns = patterns('snd.views.centro_biomedico',
    url(r'^listar$', 'listar', name='centro_biomedico_listar'),
    url(r'^finalizar/(?P<edicion>\d+)$', 'finalizar', name='centro_biomedico_finalizar'),
    url(r'^ver/(\d+)/(\d+)$', 'ver', name='centro_biomedico_ver'),

    #urls wizard
    url(r'^crear_editar/(?P<paso>\w+)/(?P<edicion>\d+)$', 'crear_editar', name='centro_biomedico_crear_editar'),
    url(r'^crear_editar/(?P<paso>\w+)/(?P<edicion>\d+)/(?P<centro_biomedico_id>\d+)$', 'crear_editar', name='centro_biomedico_crear_editar'), 
)