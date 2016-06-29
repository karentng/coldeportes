#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('api_interoperable.views',
    url(r'^deportistas/$', 'deportista_get_post', name='get_depor'),
    url(r'^deportistas/(?P<pk>[0-9]+)$', 'deportista_detail_put_delete', name='get_depor_detail'),

)
urlpatterns = format_suffix_patterns(urlpatterns)