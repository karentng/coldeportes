#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from reconocimiento_deportivo.views.solicitudes import *

urlpatterns = patterns('reconocimiento_deportivo.views.solicitudes',
    url(r'^solicitar$', 'solicitar', name='reconocimiento_deportivo_solicitar'),
    url(r'^solicitar/(\d+)$', 'solicitar', name='reconocimiento_deportivo_solicitar'),
    url(r'^listar$', 'listar_reconocimientos', name='listar_reconocimientos'),
    #url(r'^crear/adjunto/(\d+)$', 'adjuntar_archivo_solicitud', name='adjuntar_archivo_solicitud'),
    #url(r'^borrar/adjunto/(\d+)/(\d+)$', 'borrar_adjunto', name='borrar_adjunto'),
    url(r'^cancelar$', 'cancelar_solicitud_reconocimiento', name='cancelar_solicitud_reconocimiento'),
    url(r'^cancelar/(\d+)$', 'cancelar_solicitud_reconocimiento', name='cancelar_solicitud_reconociemiento'),
    url(r'^imprimir/(\d+)$', 'imprimir_solicitud', name='imprimir_reconocimiento'),


)