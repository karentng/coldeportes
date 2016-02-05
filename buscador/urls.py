from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('buscador.views',
	url(r'^centros-de-acondicionamiento$', 'centros_acondicionamiento', name='buscador_centros_acondicionamiento'),
)