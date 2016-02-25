from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('registro_resultados.views',
    url(r'^juegos/registro$', 'registrar_juego', name='registrar_juego'),
    url(r'^juegos/registro/(\d+)$', 'registrar_juego', name='registrar_juego'),
    url(r'^juegos/listar$', 'listar_juegos', name='listar_juegos'),

    url(r'^juegos/(\d+)/datos-competencia$', 'datos_competencia', name='datos_competencia'),
    url(r'^juegos/(\d+)/datos-competencia/(\d+)$', 'datos_competencia', name='datos_competencia'),
    url(r'^juegos/(\d+)/competencia/(\d+)/eliminar$', 'eliminar_competencia', name='eliminar_competencia'),
    url(r'^juegos/(\d+)/listado-competencias$', 'listado_competencias', name='listado_competencias'),
    url(r'^acceder-competencia/(\d+)$', 'acceder_competencia', name='acceder_competencia'),
    url(r'^menu-competencia$', 'menu_competencia', name='menu_competencia'),
    
    url(r'^crear-participante', 'crear_participante', name='crear_participante'),

    url(r'^datos-participante$', 'datos_participante', name='datos_participante'),
    url(r'^datos-participante/(\d+)$', 'datos_participante', name='datos_participante'),

    url(r'^datos-equipo$', 'datos_equipo', name='datos_equipo'),
    url(r'^datos-equipo/(\d+)$', 'datos_equipo', name='datos_equipo'),
)
