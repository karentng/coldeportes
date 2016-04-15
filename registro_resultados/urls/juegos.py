from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('registro_resultados.views.juegos',
    url(r'registro$', 'registrar_juego', name='registrar_juego'),
    url(r'registro/(\d+)$', 'registrar_juego', name='registrar_juego'),
    url(r'listar$', 'listar_juegos', name='listar_juegos'),
    url(r'eliminar/(\d+)$', 'eliminar_juego', name='eliminar_juego'),


    url(r'(\d+)/datos-competencia$', 'datos_competencia', name='datos_competencia'),
    #url(r'(\d+)/datos-competencia/(\d+)$', 'datos_competencia', name='datos_competencia'),
    url(r'(\d+)/competencia/(\d+)/eliminar$', 'eliminar_competencia', name='eliminar_competencia'),
    url(r'(\d+)/listado-competencias$', 'listado_competencias', name='listado_competencias'),
    
    url(r'^competencia/(\d+)/crear-participante/$', 'crear_participante', name='crear_participante'),
    url(r'^competencia/(\d+)/listar-participantes/$', 'listar_participantes', name='listar_participantes'),
    url(r'^competencia/(\d+)/medalleria/$', 'medalleria_por_competencia', name='medalleria_por_competencia'),

    url(r'^competencia/(\d+)/listar-individual/$', 'listar_individual', name='listar_individual'),
    url(r'^competencia/(\d+)/listar-equipos/$', 'listar_equipos', name='listar_equipos'),

    url(r'^competencia/(\d+)/datos-participante$', 'datos_participante', name='datos_participante'),
    url(r'^competencia/(\d+)/participante-tiempos$', 'participante_tiempos', name='participante_tiempos'),
    url(r'^competencia/(\d+)/participante-tiempos/(\d+)$', 'participante_tiempos', name='participante_tiempos'),
    url(r'^competencia/(\d+)/participantes-puntos$', 'participante_puntos', name='participante_puntos'),
    url(r'^competencia/(\d+)/participantes-puntos/(\d+)$', 'participante_puntos', name='participante_puntos'),
    url(r'^competencia/(\d+)/participantes-metros$', 'participante_metros', name='participante_metros'),
    url(r'^competencia/(\d+)/participantes-metros/(\d+)$', 'participante_metros', name='participante_metros'),
    url(r'^competencia/(\d+)/eliminar-participante/(\d+)$', 'eliminar_participante', name='eliminar_participante'),

    url(r'^competencia/(\d+)/datos-equipo$', 'datos_equipo', name='datos_equipo'),
    url(r'^competencia/(\d+)/equipo-tiempos$', 'equipo_tiempos', name='equipo_tiempos'),
    url(r'^competencia/(\d+)/equipo-tiempos/(\d+)$', 'equipo_tiempos', name='equipo_tiempos'),
    url(r'^competencia/(\d+)/equipo-puntos$', 'equipo_puntos', name='equipo_puntos'),
    url(r'^competencia/(\d+)/equipo-puntos/(\d+)$', 'equipo_puntos', name='equipo_puntos'),
    url(r'^competencia/(\d+)/equipo-metros$', 'equipo_metros', name='equipo_metros'),
    url(r'^competencia/(\d+)/equipo-metros/(\d+)$', 'equipo_metros', name='equipo_metros'),
    url(r'^competencia/(\d+)/eliminar-equipo/(\d+)$', 'eliminar_equipo', name='eliminar_equipo'),
    
    #ajax para modalidades y categorías
    url(r'^modalidades/get/(\d+)$','get_modalidades',name='registro_get_modalidades'),
    url(r'^categorias/get/(\d+)$','get_categorias',name='registro_get_categorias'),

    
    url(r'^competencia/(\d+)/equipo/(\d+)/participantes$', 'participante_equipo', name='participante_equipo'),

    url(r'^competencia/(\d+)/equipo/(\d+)/participantes(\d+)$', 'participante_equipo', name='participante_equipo'),

    # cargado por excel
    url(r'^cargar-competencias/(\d+)$', 'cargas_competencias', name='cargas_competencias'),
    url(r'^cargar-participantes/(\d+)$', 'cargar_participantes', name='cargar_participantes'),
)
