from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.personal_apoyo import *



urlpatterns = patterns('snd.views.personal_apoyo',

    #Urls de Wizard
    url(r'^wizard/identificacion$', 'wizard_personal_apoyo_nuevo', name='personal_apoyo_nuevo'),
    url(r'^wizard/identificacion/(\d+)$', 'wizard_personal_apoyo', name='edicion_personal_apoyo'),
    url(r'^wizard/formacion-deportiva/(\d+)$', 'wizard_formacion_deportiva', name='wizard_formacion_deportiva'),
    url(r'^wizard/experiencia-laboral/(\d+)$', 'wizard_experiencia_laboral', name='wizard_experiencia_laboral'),

    #Urls de eliminacion de muchos en el wizard
    url(r'^eliminar/formacion-deportiva/(\d+)/(\d+)$', 'eliminar_formacion_deportiva', name='eliminar_formacion_deportiva'),
    url(r'^eliminar/experiencia-laboral/(\d+)/(\d+)$', 'eliminar_experiencia_laboral', name='eliminar_experiencia_laboral'),

    #Urls de listado y desactivacion
    url(r'^listar$', 'listar_personal_apoyo', name='personal_apoyo_listar'),
    url(r'^desactivar/(\d+)$', 'desactivar_personal_apoyo', name='personal_apoyo_desactivar'),
    url(r'^finalizar/(?P<opcion>.+)', 'finalizar_personal_apoyo', name='finalizar_personal_apoyo'),
    url(r'^ver/(\d+)/(\d+)$','ver_personal_apoyo',name='ver_personal_apoyo'),
    url(r'^verificar$', 'verificar_personal_apoyo', name='verificar_personal_apoyo'),
)
