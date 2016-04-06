from django.conf.urls import patterns, url

"""
Autor: Cristian Leonardo Ríos López
"""

urlpatterns = patterns(
    'snd.views.escuela_deportiva',

    # urls sedes
    url(r'^sedes/listar$', 'listar', name='escuela_deportiva_listar'),
    url(r'^sedes/finalizar/(?P<edicion>\d+)$', 'finalizar', name='escuela_deportiva_finalizar'),
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
    url(r'^sedes/crear_editar/(?P<paso>\w+)/(?P<edicion>\d+)$', 'crear_editar', name='escuela_deportiva_crear_editar'),
    url(r'^sedes/crear_editar/(?P<paso>\w+)/(?P<edicion>\d+)/(?P<escuela_deportiva_id>\d+)$', 'crear_editar', name='escuela_deportiva_crear_editar'),
)