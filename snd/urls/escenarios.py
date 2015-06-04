from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.escenarios import *


urlpatterns = patterns('snd.views.escenarios',
    #urls para crear escenarios
    url(r'^nuevo/identificacion$', 'nuevo_identificacion', name='nuevo_identificacion'),
    url(r'^nuevo/caracterizacion/(\d+)$', 'nuevo_caracterizacion', name='nuevo_caracterizacion'),

    url(r'^listar$', 'listarEscenarios', name='listar_escenarios'), 
    url(r'^desactivar/(\d+)$', 'desactivarEscenario', name='desactivar_escenario'),
    #urls de editar escenarios
    url(r'^editar/identificacion/(\d+)$', 'editar_identificacion', name='editar_identificacion'), 
    url(r'^editar/caracterizacion/(\d+)$', 'editar_caracterizacion', name='editar_caracterizacion'), 
    url(r'^editar/horarios/(\d+)$', 'editar_horarios', name='editar_horarios'), 
    url(r'^editar/fotos/(\d+)$', 'editar_fotos', name='editar_fotos'), 
    url(r'^editar/videos/(\d+)$', 'editar_videos', name='editar_videos'), 
    url(r'^editar/historicos/(\d+)$', 'editar_historicos', name='editar_historicos'), 
    url(r'^editar/contactos/(\d+)$', 'editar_contactos', name='editar_contactos'), 
    #urls para eliminar los pasos de los que se pueden registrar muchos en el wizard
    url(r'^eliminar/horario/(\d+)/(\d+)$', 'eliminar_horario', name='eliminar_horario'), 
    url(r'^eliminar/historico/(\d+)/(\d+)$', 'eliminar_historico', name='eliminar_historico'), 
    url(r'^eliminar/foto/(\d+)/(\d+)$', 'eliminar_foto', name='eliminar_foto'), 
    url(r'^eliminar/video/(\d+)/(\d+)$', 'eliminar_video', name='eliminar_video'), 
    url(r'^eliminar/contacto/(\d+)/(\d+)$', 'eliminar_contacto', name='eliminar_contacto'), 

)
