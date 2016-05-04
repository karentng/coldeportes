#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from reconocimiento_deportivo.views import solicitudes

urlpatterns = patterns('reconocimiento_deportivo.views.solicitudes',
    url(r'^solicitar$', 'solicitar', name='reconocimiento_deportivo_solicitar'),
    url(r'^solicitar/(\d+)$', 'solicitar', name='reconocimiento_deportivo_solicitar'),
    url(r'^discusion/(\d+)$', 'editar_solicitud', name='editar_solicitud_reconocimiento'),
    url(r'^listar$', 'listar_reconocimientos', name='listar_reconocimientos'),
    url(r'^cancelar$', 'cancelar_solicitud', name='cancelar_solicitud_reconocimiento'),
    url(r'^cancelar/(\d+)$', 'cancelar_solicitud', name='cancelar_solicitud_reconocimiento'),
    url(r'^imprimir/(\d+)$', 'imprimir_solicitud', name='imprimir_reconocimiento'),
    url(r'^finalizar/(\d+)$', 'finalizar_solicitud', name='finalizar_solicitud_reconocimiento'),
    url(r'^ver/(\d+)$', 'ver_solicitud', name='ver_solicitud_reconocimiento'),
    url(r'^(\d+)/discusion$', 'enviar_comentario', name='enviar_comentario_reconocimiento'),
    
    url(r'^adjuntar/(\d+)$', 'adjuntar_requerimientos', name='adjuntar_requerimientos_reconocimiento'),
    url(r'^(\d+)/borrar/adjunto/(\d+)$', 'borrar_adjunto', name='borrar_adjunto_reconocimiento'),
    url(r'^(\d+)/descargar/adjunto/(\d+)$', 'descargar_adjunto', name='descargar_adjunto_reconocimiento'),
    url(r'^(\d+)/descargar-adjuntos$', 'descargar_adjuntos', name='descargar_adjuntos_reconocimiento'),
    url(r'^(\d+)/descargar-adjuntos-discusion/(\d+)$', 'descargar_adjunto_discusion', name='descargar_adjunto_discusion_reconocimiento'),


)