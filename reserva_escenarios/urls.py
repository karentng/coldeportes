#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from reconocimiento_deportivo.views import solicitudes

urlpatterns = patterns('reserva_escenarios.views',
    url(r'^listar-escenarios$', 'listar_escenarios', name='listar_escenarios_reservas'),
    url(r'^listar-solicitudes$', 'listar_solicitudes', name='listar_solicitudes_reservas'),
    url(r'^solicitar$', 'solicitar_reserva', name='solicitar_reserva'),
    url(r'^agendar-reserva/(\d+)$', 'agendar_reserva', name='agendar_reserva'),
    url(r'^responder-solicitud/(\d+)$', 'responder_solicitud', name='responder_solicitud_reserva'),
    url(r'^guardar/(\d+)$', 'guardar_fechas_reserva', name='guardar_fechas_reserva'),
    url(r'^configurar-reservas/(\d+)$', 'configurar_reservas', name='configurar_reservas'),
    url(r'^imprimir-reserva/(\d+)$', 'imprimir_solicitud', name='imprimir_solicitud_reservas'),
)