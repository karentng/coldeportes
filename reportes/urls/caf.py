#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.caf',
	url(r'^caracteristicas-caf$', 'caracteristicas_caf', name='reportes_caracteristicas_caf'),
)