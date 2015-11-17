from django.conf.urls import patterns, include, url

urlpatterns = patterns('normograma.views',
    url(r'^registrar$', 'registrar', name='normograma_registrar'),
    url(r'^buscar$', 'buscar', name='normograma_buscar'),
    url(r'^editar/(\d+)$', 'editar', name='editar_norma'),

)