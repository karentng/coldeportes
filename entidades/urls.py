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
)
