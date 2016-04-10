from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('calendario_deportivo.views',
    #url(r'^$', 'cargar_calendario', name='cargar_calendario_nacional'),
    url(r'^$', 'public', name='public_calendar'),


)
