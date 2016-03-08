#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views.dirigentes',
	url(r'^nacionalidad-dirigentes$', 'nacionalidad_dirigentes', name='reportes_nacionalidad_dirigentes'),
	url(r'^cantidad-dirigentes$', 'cantidad_dirigentes', name='reportes_cantidad_dirigentes'),
)