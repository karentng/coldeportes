from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('entidades.views',
	url(r'^tipo$', 'tipo', name='entidad_tipo'),
    url(r'^registro/(\d+)$', 'registro', name='entidad_registro'),
    url(r'^test/$', 'test', name='test'),
    url(r'^cafs/$', 'cafs', name='cafs'),
    url(r'^sincronizar/$', 'sincronizar', name='sincronizar'),
    url(r'^localizacion/$', 'actualizarLocalizacion', name='actualizarLocalizacion'),
)
