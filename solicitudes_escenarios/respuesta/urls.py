from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('solicitudes_escenarios.respuesta.views',
    url(r'^listar$', 'listar_solicitudes', name='listar_solicitudes'),

)
