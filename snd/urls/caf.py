#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.caf import *
from snd.formularios.caf  import *
from coldeportes.utilities import all_permission_required


urlpatterns = patterns('snd.views.caf',
    url(r'^crear-editar/(?P<paso>\w+)$', 'crear', name='crear_caf'),
    url(r'^crear-editar/(?P<paso>\w+)/(?P<idCAF>\d+)$', 'crear', name='crear_caf'),
    url(r'^finalizar/(\d+)$', 'finalizar', name='finalizar_caf'),

    url(r'^crear-plan/(\d+)$', 'crear_plan', name='crear_plan'),
    url(r'^eliminar-plan/(\d+)/(\d+)$', 'eliminar_plan', name='eliminar_plan'),

    url(r'^crear-foto/(\d+)$', 'crear_foto', name='crear_foto'),
    url(r'^eliminar-foto/(\d+)/(\d+)$', 'eliminar_foto_caf', name='eliminar_foto_caf'),
    

    url(r'^listar$', 'listarCAFS', name='listar_cafs'),
    url(r'^ver/(\d+)/(\d+)$', 'ver_caf', name='ver_caf'),

    url(r'^desactivar-caf/(\d+)$', 'desactivar_caf', name='desactivar_caf'),

    url(r'^georreferenciacion$', 'georreferenciacion_caf', name='georreferenciacion_caf'),
    #url(r'^desactivar/(\d+)$', 'desactivarCAF', name='desactivar_caf'),
)
