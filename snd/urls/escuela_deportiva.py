from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.escuela_deportiva import *

"""
Autor: Cristian Leonardo Ríos López
"""

urlpatterns = patterns(
    'snd.views.escuela_deportiva',

    # urls sedes
    url(r'^escuela-deportiva/sedes/listar$', 'listar', name='escuela_deportiva_listar'),
    url(r'^escuela-deportiva/sedes/finalizar/(?P<edicion>\d+)$', 'finalizar', name='escuela_deportiva_finalizar'),
    url(r'^escuela-deportiva/sedes/ver/(\d+)/(\d+)$', 'ver', name='escuela_deportiva_ver'),
    url(r'^escuela-deportiva/sedes/desactivar/(\d+)$', 'desactivar_escuela_deportiva', name='escuela_deportiva_desactivar'),

    # urls participantes
    url(r'^escuela-deportiva/participantes/registrar', 'registrar_participante', name='registrar_participante'),
    url(r'^escuela-deportiva/participantes/listar$', 'listar_participante', name='listar_participante'),

    # urls wizard
    url(r'^escuela-deportiva/sedes/crear_editar/(?P<paso>\w+)/(?P<edicion>\d+)$', 'crear_editar', name='escuela_deportiva_crear_editar'),
    url(r'^escuela-deportiva/sedes/crear_editar/(?P<paso>\w+)/(?P<edicion>\d+)/(?P<escuela_deportiva_id>\d+)$', 'crear_editar', name='escuela_deportiva_crear_editar'),
)