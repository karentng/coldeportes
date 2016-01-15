#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.escuelas',
	url(r'^estrato-escuelas$', 'estrato_escuelas', name='reportes_estrato_escuelas'),
	url(r'^servicios-escuelas$', 'servicios_escuelas', name='reportes_servicios_escuelas'),
)