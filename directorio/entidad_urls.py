from django.conf.urls import patterns, include, url

urlpatterns = patterns('directorio.views.entidad',
    url(r'^buscar', 'directorio_buscar', name='directorio_buscar'),
    #url(r'^ver', 'directorio_ver_detalles', name='directorio_ver_detalles'),

)