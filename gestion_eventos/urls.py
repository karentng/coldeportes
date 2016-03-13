from django.conf.urls import patterns, include, url

urlpatterns = patterns('gestion_eventos.views',
                       url(r'^registrar$', 'registrar_evento', name='registrar_evento'),
                       url(r'^listar$', 'listar_eventos', name='listar_eventos'),
                       url(r'^editar/(\d+)$', 'editar_evento', name='editar_evento'),
                       url(r'^verificar/(\d+)$', 'verificar_participante', name='verificar_participante'),
                       url(r'^preinscripcion/(\d+)$', 'preinscripcion_evento', name='preinscripcion_evento'),
                       url(r'^editar-participante/(\d+)$', 'editar_participante', name='editar_participante'),
                       url(r'^listar-participantes/(\d+)$', 'listar_participantes', name='listar_participantes'),
                       url(r'^registrar-actividad/(\d+)$', 'registrar_actividad', name='registrar_actividad'),
                       url(r'^editar-actividad/(\d+)$', 'editar_actividad', name='editar_actividad'),
                       url(r'^ver-actividades/(\d+)$', 'ver_actividades', name='ver_actividades'),
                       url(r'^cambio-fecha-actividad$', 'cambio_fecha_actividad', name='cambio_fecha_actividad'),
                       )
