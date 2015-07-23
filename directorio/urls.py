from django.conf.urls import patterns, include, url

urlpatterns = patterns('directorio.views',
    url(r'^buscar', 'directorio_buscar', name='directorio_buscar'),

)