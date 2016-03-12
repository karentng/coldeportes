from django.conf.urls import patterns, include, url

urlpatterns = patterns('gestion_eventos.views',
                       url(r'^registrar$', 'registrar_evento', name='registrar_evento'),
                       url(r'^listar$', 'listar_eventos', name='listar_eventos'),
                       url(r'^verificar/(\d+)$', 'verificar_participante', name='verificar_participante'),
                       url(r'^preinscripcion/(\d+)$', 'preinscripcion_evento', name='preinscripcion_evento'),
                       url(r'^listar-participantes/(\d+)$', 'listar_participantes', name='listar_participantes'),
                       )
