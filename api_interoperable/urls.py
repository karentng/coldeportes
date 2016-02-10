#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('api_interoperable.views',
    url(r'^get-dep', 'get_deportista', name='get_depor'),

)