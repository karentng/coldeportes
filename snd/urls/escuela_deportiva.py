from django.conf.urls import patterns, url

"""
Autor: Cristian Leonardo Ríos López
"""

urlpatterns = patterns(
    'snd.views.escuela_deportiva',

    # urls sedes
    url(r'^sedes/listar$', 'listar', name='escuela_deportiva_listar'),
    url(r'^sedes/finalizar/(\d+)/(\w+)$', 'finalizar', name='finalizar_sede'),
    url(r'^sedes/ver/(\d+)/(\d+)$', 'ver', name='escuela_deportiva_ver'),
    url(r'^sedes/desactivar/(\d+)$', 'desactivar_escuela_deportiva',
        name='escuela_deportiva_desactivar'),
    url(r'^ajax-sedes-categorias', 'ajax_categoria_sede', name='ajax_categoria_sede'),

    # urls participantes
    url(r'^participantes/registrar', 'registrar_participante', name='registrar_participante'),
    url(r'^participantes/listar$', 'listar_participante', name='listar_participante'),
    url(r'^participantes/editar/(\d+)$', 'editar_participante', name='editar_participante'),
    url(r'^participantes/detalles/(\d+)$', 'detalles_participante', name='detalles_participante'),
    url(r'^participantes/cambiar-estado/(\d+)$', 'cambiar_estado_participante', name='cambiar_estado_participante'),
    url(r'^gestion-alertas/(\d+)$', 'gestion_alertas', name='gestion_alertas'),
    url(r'^estado-alerta/(\d+)$', 'cambiar_estado_alerta', name='cambiar_estado_alerta'),
    url(r'^registro-typ/(\d+)$', 'registrar_typ', name='registrar_typ'),
    url(r'^eliminacion-typ/(\d+)$', 'eliminar_typ', name='eliminar_typ'),
    url(r'^ajax-alerta', 'ajax_alerta', name='ajax_alerta'),


    # urls acudientes
    url(r'^acudiente/registrar/(\d+)$', 'registrar_acudiente', name='registrar_acudiente'),
    url(r'^acudiente/listar$', 'listar_acudientes', name='listar_acudientes'),
    url(r'^acudiente/editar/(\d+)$', 'editar_acudiente', name='editar_acudiente'),
    url(r'^acudiente/cambiar-estado/(\d+)$', 'cambiar_estado_acudiente', name='cambiar_estado_acudiente'),

    # urls actividades
    url(r'^actividades/registrar$', 'registrar_actividadefd', name='registrar_actividadefd'),
    url(r'^actividades/editar/(\d+)$', 'editar_actividadefd', name='editar_actividadefd'),
    url(r'^actividades/listar', 'listar_actividadesefd', name='listar_actividadesefd'),
    url(r'^actividades/cambiar-estado/(\d+)$', 'cambiar_estado_actividadefd', name='cambiar_estado_actividadefd'),
    url(r'^actividades/asistencia/(\d+)$', 'listado_asistencia_actividad', name='listado_asistencia_actividad'),
    url(r'^actividades/ajax-asistencia$', 'ajax_asistencia', name='ajax_asistencia'),

    # urls wizard
    url(r'^wizard/sede$', 'wizard_nuevo_sede', name='wizard_nuevo_sede'),
    url(r'^wizard/sede/(\d+)$', 'wizard_sede', name='wizard_sede'),
    url(r'^wizard/servicios/(\d+)$', 'wizard_servicios_sede', name='wizard_servicios'),
    url(r'^wizard/categorias/(\d+)$', 'wizard_categorias_sede', name='wizard_categorias_sede'),
    url(r'^wizard/horarios/(\d+)$', 'wizard_horarios_sede', name='wizard_horarios_sede'),
    url(r'^eliminar/horario/(\d+)/(\d+)$', 'eliminar_horario_sede', name='eliminar_horario_sede'),
    url(r'^eliminar/categoria/(\d+)/(\d+)$', 'eliminar_categoria_sede', name='eliminar_categoria_sede'),
)
