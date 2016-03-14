from django.conf.urls import patterns, include, url

urlpatterns = patterns('listados_doping.views',
    url(r'^registrar$', 'registrar_caso_doping', name='registrar_caso_doping'),
    url(r'^listar$', 'listar_casos_doping', name='listar_casos_doping'),
    url(r'^editar/(\d+)$', 'editar_caso_doping', name='editar_caso_doping'),
    url(r'^cambiar_estado/(\d+)$', 'cambiar_estado_caso_doping', name='cambiar_estado_caso_doping'),
)
