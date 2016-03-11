from django.conf.urls import patterns, include, url

urlpatterns = patterns('gestion_eventos.views',
                       url(r'^registrar$', 'registrar_evento', name='registrar_evento'),
                       url(r'^listar$', 'listar_eventos', name='listar_eventos'),
                       )
