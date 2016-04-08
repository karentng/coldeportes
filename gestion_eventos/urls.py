from django.conf.urls import patterns, include, url

urlpatterns = patterns('gestion_eventos.views',
                       url(r'^dashboard/(\d+)$', 'dashboard', name='dashboard'),
                       url(r'^registrar$', 'registrar_evento', name='registrar_evento'),
                       url(r'^listar$', 'listar_eventos', name='listar_eventos'),
                       url(r'^editar/(\d+)$', 'editar_evento', name='editar_evento'),
                       url(r'^detalle/(\d+)$', 'detalle_evento', name='detalle_evento'),
                       url(r'^cambiar-estado-evento/(\d+)$', 'cambiar_estado_evento', name='cambiar_estado_evento'),
                       url(r'^verificar/(\d+)$', 'verificar_participante', name='verificar_participante'),
                       url(r'^preinscripcion/(\d+)$', 'preinscripcion_evento', name='preinscripcion_evento'),
                       url(r'^editar-participante/(\d+)$', 'editar_participante', name='editar_participante'),
                       url(r'^listar-participantes/(\d+)$', 'listar_participantes', name='listar_participantes'),
                       url(r'^aceptar-candidato/(\d+)$', 'aceptar_candidato', name='aceptar_candidato'),
                       url(r'^confirmar-participacion/(\d+)$', 'confirmar_participacion', name='confirmar_participacion'),
                       url(r'^gestion-pago/(\d+)$', 'gestion_pago', name='gestion_pago'),
                       url(r'^generar-entrada/(\d+)$', 'generar_entrada', name='generar_entrada'),
                       url(r'^registrar-actividad/(\d+)$', 'registrar_actividad', name='registrar_actividad'),
                       url(r'^editar-actividad/(\d+)$', 'editar_actividad', name='editar_actividad'),
                       url(r'^ver-actividades/(\d+)$', 'ver_actividades', name='ver_actividades'),
                       url(r'^cambio-fecha-actividad$', 'cambio_fecha_actividad', name='cambio_fecha_actividad'),
                       url(r'^cambiar-estado-actividad/(\d+)$', 'cambiar_estado_actividad', name='cambiar_estado_actividad'),
                       url(r'^registrar-resultado/(\d+)$', 'registrar_resultado', name='registrar_resultado'),
                       url(r'^editar-resultado/(\d+)$', 'editar_resultado', name='editar_resultado'),
                       url(r'^cambiar-estado-resultado/(\d+)$', 'cambiar_estado_resultado', name='cambiar_estado_resultado'),
                       )