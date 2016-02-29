from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('registro_resultados.views',
    url(r'registro$', 'registrar_juego', name='registrar_juego'),
    url(r'registro/(\d+)$', 'registrar_juego', name='registrar_juego'),
    url(r'listar$', 'listar_juegos', name='listar_juegos'),

    url(r'(\d+)/datos-competencia$', 'datos_competencia', name='datos_competencia'),
    url(r'(\d+)/datos-competencia/(\d+)$', 'datos_competencia', name='datos_competencia'),
    url(r'(\d+)/competencia/(\d+)/eliminar$', 'eliminar_competencia', name='eliminar_competencia'),
    url(r'(\d+)/listado-competencias$', 'listado_competencias', name='listado_competencias'),
    
    url(r'^(\d+)/competencia/(\d+)/crear-participante/', 'crear_participante', name='crear_participante'),

    url(r'^(\d+)/competencia/(\d+)/datos-participante$', 'datos_participante', name='datos_participante'),
    url(r'^(\d+)/competencia/(\d+)/datos-participante/(\d+)$', 'datos_participante', name='datos_participante'),

    url(r'^(\d+)/competencia/(\d+)/datos-equipo$', 'datos_equipo', name='datos_equipo'),
    url(r'^(\d+)/competencia/(\d+)/datos-equipo/(\d+)$', 'datos_equipo', name='datos_equipo'),
    #ajax para modalidades y categorías
    url(r'^modalidades/get/(\d+)$','get_modalidades',name='registro_get_modalidades'),
    url(r'^categorias/get/(\d+)$','get_categorias',name='registro_get_categorias'),

    url(r'^acceder-competencia/(\d+)$', 'acceder_competencia', name='acceder_competencia'),
    url(r'^menu-competencia$', 'menu_competencia', name='menu_competencia'),
)
