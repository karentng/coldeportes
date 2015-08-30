from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.selecciones import *

urlpatterns = patterns('snd.views.selecciones',
    url(r'^registro/base$', 'registrar_base', name='registrar_seleccion'),
)
