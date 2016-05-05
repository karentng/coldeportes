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

    # urls participantes
    url(r'^participantes/registrar', 'registrar_participante', name='registrar_participante'),
    url(r'^participantes/listar$', 'listar_participante', name='listar_participante'),
    url(r'^participantes/editar/(\d+)$', 'editar_participante', name='editar_participante'),
    url(r'^participantes/detalles/(\d+)$', 'detalles_participante', name='detalles_participante'),
    url(r'^participantes/cambiar-estado/(\d+)$', 'cambiar_estado_participante',
        name='cambiar_estado_participante'),

    # urls acudientes
    url(r'^acudiente/registrar/(\d+)$', 'registrar_acudiente',
        name='registrar_acudiente'),
    url(r'^acudiente/listar$', 'listar_acudientes', name='listar_acudientes'),
    url(r'^acudiente/editar/(\d+)$', 'editar_acudiente', name='editar_acudiente'),
    url(r'^acudiente/cambiar-estado/(\d+)$', 'cambiar_estado_acudiente',
        name='cambiar_estado_acudiente'),

    # urls wizard
    url(r'^wizard/sede$', 'wizard_nuevo_sede', name='wizard_nuevo_sede'),
    url(r'^wizard/sede/(\d+)$', 'wizard_sede', name='wizard_sede'),
    url(r'^wizard/servicios/(\d+)$', 'wizard_servicios_sede', name='wizard_servicios'),
    url(r'^wizard/categorias/(\d+)$', 'wizard_categorias_sede', name='wizard_categorias_sede'),
    url(r'^wizard/horarios/(\d+)$', 'wizard_horarios_sede', name='wizard_horarios_sede'),
    url(r'^eliminar/horario/(\d+)/(\d+)$', 'eliminar_horario_sede', name='eliminar_horario_sede'),
    url(r'^eliminar/categoria/(\d+)/(\d+)$', 'eliminar_categoria_sede', name='eliminar_categoria_sede'),
)
