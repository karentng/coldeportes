from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.escuela_deportiva import *

"""
Autor: Cristian Leonardo Ríos López
"""

urlpatterns = patterns('snd.views.escuela_deportiva',
    url(r'^listar$', 'listar', name='escuela_deportiva_listar'),
    url(r'^finalizar/(?P<edicion>\d+)$', 'finalizar', name='escuela_deportiva_finalizar'),
    url(r'^ver/(\d+)/(\d+)$', 'ver', name='escuela_deportiva_ver'),

    #urls wizard
    url(r'^crear_editar/(?P<paso>\w+)/(?P<edicion>\d+)$', 'crear_editar', name='escuela_deportiva_crear_editar'),
    url(r'^crear_editar/(?P<paso>\w+)/(?P<edicion>\d+)/(?P<escuela_deportiva_id>\d+)$', 'crear_editar', name='escuela_deportiva_crear_editar'), 
)