from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('solicitudes_escenarios.solicitud.views',
    url(r'^crear$', 'generar_solicitud', name='generar_solicitud'),
    url(r'^crear/(\d+)$', 'generar_solicitud', name='generar_solicitud'),
    url(r'^listar$', 'listar_solicitudes', name='listar_solicitudes'),
    url(r'^crear/adjunto/(\d+)$', 'adjuntar_archivo_solicitud', name='adjuntar_archivo_solicitud'),
    url(r'^borrar/adjunto/(\d+)/(\d+)$', 'borrar_adjunto', name='borrar_adjunto'),
    url(r'^cancelar$', 'cancelar_solicitud', name='cancelar_solicitud'),
    url(r'^cancelar/(\d+)$', 'cancelar_solicitud', name='cancelar_solicitud'),
    url(r'^finalizar/(\d+)$', 'finalizar_solicitud', name='finalizar_solicitud'),
    url(r'^imprimir/(\d+)$', 'imprimir_solicitud', name='imprimir_solicitud'),

)
