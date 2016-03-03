from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('solicitudes_escenarios.respuesta.views',
    url(r'^listar$', 'listar_solicitudes', name='listar_solicitudes_respuesta'),
    url(r'^ver/(\d+)/(\d+)$', 'ver_solicitud', name='ver_solicitud_respuesta'),
    url(r'^imprimir/(\d+)/(\d+)$', 'imprimir_solicitud', name='imprimir_solicitud_respuesta'),
    url(r'^descargar/(\d+)/(\d+)/(\d+)$', 'descargar_adjunto', name='descargar_adjunto_respuesta'),
    url(r'^responder/(\d+)/(\d+)$', 'responder_solicitud', name='responder_solicitud'),
    url(r'^comentar/(\d+)/(\d+)$', 'enviar_respuesta', name='enviar_respuesta'),


)
