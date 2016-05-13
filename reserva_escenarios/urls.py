#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from reconocimiento_deportivo.views import solicitudes

urlpatterns = patterns('reserva_escenarios.views',
    url(r'^listar-escenarios$', 'listar_escenarios', name='listar_escenarios_reservas'),
    url(r'^calendario/(\d+)$', 'calendario_reservas', name='calendario_reservas'),
    url(r'^solicitar-reserva/(\d+)$', 'solicitar_reserva', name='solicitar_reserva'),
)