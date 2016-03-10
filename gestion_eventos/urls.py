from django.conf.urls import patterns, include, url

urlpatterns = patterns('noticias.views',
                       url(r'^registrar$', 'registrar_evento', name='registrar_evento'),
                       url(r'^listar$', 'listar_noticias', name='listar_noticias'),
                       )
