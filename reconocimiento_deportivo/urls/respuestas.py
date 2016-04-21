#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('reconocimiento_deportivo.views.respuestas',
    url(r'^listar-solicitudes$', 'listar_solicitudes_reconocimientos', name='listar_solicitudes_reconocimientos'),
    url(r'^responder/(\d+)/(\d+)$', 'responder_solicitud_reconocimiento', name='responder_solicitud_reconocimiento'),
    url(r'^ver/(\d+)/(\d+)$', 'ver_solicitud_reconocimiento', name='ver_solicitud_reconocimiento_respuesta'),
    url(r'^imprimir/(\d+)/(\d+)$', 'imprimir_solicitud', name='imprimir_solicitud_reconocimiento'),
    url(r'^enviar-respuesta/(\d+)/(\d+)$', 'enviar_respuesta', name='enviar_respuesta_reconocimiento'),
    url(r'^descargar-adjunto-respuesta/(\d+)/(\d+)/(\d+)$', 'descargar_adjunto', name='descargar_adjunto_reconocimiento_respuesta'),
    url(r'^descargar-adjuntos/(\d+)/(\d+)$', 'descargar_todos_adjuntos', name='descargar_todos_adjuntos_reconocimiento_respuesta'),
    url(r'^descargar-adjuntos-respuesta/(\d+)/(\d+)$', 'descargar_adjuntos_respuesta', name='descargar_adjuntos_reconocimiento_respuesta'),

)