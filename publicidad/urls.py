from django.conf.urls import patterns, include, url

urlpatterns = patterns('publicidad.views',
    url(r'^registrar$', 'registrar_clasificado', name='registrar_clasificado'),
    url(r'^listar$', 'listar_clasificados', name='listar_clasificados'),
    url(r'^gestionar', 'gestionar_clasificados', name='gestionar_clasificados'),
    url(r'^editar/(\d+)$', 'editar_clasificado', name='editar_clasificado'),
    url(r'^cambiar_estado/(\d+)$', 'cambiar_estado_clasificado', name='cambiar_estado_clasificado'),
    url(r'^crop-pic$','crop_pic',name='crop_pic'),
    url(r'^filtrar$','filtro_clasificados', name='filtro_clasificados'),
)
