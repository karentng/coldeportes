from django.conf.urls import patterns, include, url

urlpatterns = patterns('noticias.views',
	url(r'^registrar$', 'registrar_noticia', name='registrar_noticia'),
	url(r'^listar$', 'listar_noticias', name='listar_noticias'),
    url(r'^editar/(\d+)$', 'editar_noticia', name='editar_noticia'),
    url(r'^eliminar/(\d+)$', 'eliminar_noticia', name='eliminar_noticia'),
)
