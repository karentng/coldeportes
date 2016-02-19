from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('solicitudes_escenarios.solicitud.views',
    url(r'^crear$', 'generar_solicitud', name='generar_solicitud'),
    url(r'^listar$', 'listar_solicitudes', name='listar_solicitudes'),

)
