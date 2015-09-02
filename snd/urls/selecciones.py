from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.selecciones import *

urlpatterns = patterns('snd.views.selecciones',
    url(r'^registro/base$', 'registrar_base', name='registrar_seleccion'),
    url(r'^edicion/base/(\d+)$', 'editar_base', name='editar_seleccion'),
    url(r'^registro/deportistas-seleccion/(\d+)$', 'registrar_deportistas', name='registrar_deportistas'),
    url(r'^registro/personal/(\d+)$', 'registrar_personal', name='registrar_personal'),
    url(r'^listar$', 'listar_seleccion', name='listar_seleccion'),
    url(r'^ver/(\d+)$', 'ver_seleccion', name='ver_seleccion'),
    url(r'^finalizar$', 'finalizar_registro_seleccion', name='finalizar_registro_seleccion'),

    #URLS para AJAX selecciones
        #URLS AJAX SELECCION DEPORTISTAS
    url(r'^vista-previa-depor/(\d+)/(\d+)$', 'vista_previa_deportista', name='vista_previa_deportista'),
    url(r'^guardar-deportista/(\d+)/(\d+)/(\d+)$', 'seleccionar_deportista', name='seleccionar_deportista'),
    url(r'^borrar-deportista/(\d+)/(\d+)/(\d+)$', 'quitar_deportista', name='quitar_deportista'),
        #URLS AJAX SELECCION PERSONAL
    url(r'^vista-previa-per/(\d+)/(\d+)$', 'vista_previa_personal', name='vista_previa_personal'),
    url(r'^guardar-personal/(\d+)/(\d+)/(\d+)$', 'seleccionar_personal', name='selecvionar_personal'),
)
