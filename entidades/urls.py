from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('entidades.views',
	url(r'^tipo$', 'tipo', name='entidad_tipo'),
    url(r'^registro/(\d+)$', 'registro', name='entidad_registro'),

    url(r'^editar/(\d+)$', 'editar', name='entidad_editar'),
    url(r'^listar$', 'listar', name='entidad_listar'),
    
    url(r'^appMovil/login/$', 'appMovilLogin', name='app_movil_login'),
    url(r'^appMovil/obtenerActores/$', 'appMovilObtenerActores', name='app_movil_obtener_actores'),
    url(r'^appMovil/sincronizar/$', 'appMovilSincronizar', name='app_movil_sincronizar'),
    url(r'^appMovil/actualizarLocalizacion/$', 'appMovilActualizarLocalizacion', name='app_movil_actualizar_localizacion'),

	url(r'^entrenadores', 'listar_entrenadores_nacionales', name='listar_entrenadores_nacionales'),
	url(r'^deportistas$', 'listar_deportistas_nacionales', name='listar_deportistas_nacionales'),
	url(r'^escenarios$', 'listar_escenarios_nacionales', name='listar_escenarios_nacionales'),
	url(r'^dirigentes$', 'listar_dirigentes_nacionales', name='listar_dirigentes_nacionales'),
	url(r'^cafs$', 'listar_cafs_nacionales', name='listar_cafs_nacionales'),
	url(r'^cajas-compensacion$', 'listar_cajas_nacionales', name='listar_cajas_nacionales'),
)
