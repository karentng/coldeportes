#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('reconocimiento_deportivo.views.respuestas',
    url(r'^listar-solicitudes$', 'listar_solicitudes_reconocimientos', name='listar_solicitudes_reconocimientos'),
    url(r'^responder/(\d+)/(\d+)$', 'responder_solicitud_reconocimiento', name='responder_solicitud_reconocimiento'),

)