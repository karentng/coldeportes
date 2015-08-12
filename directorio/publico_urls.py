from django.conf.urls import patterns, include, url

urlpatterns = patterns('directorio.views.publico',
    url(r'^buscar', 'directorio_buscar', name='directorio_publico_buscar'),

)