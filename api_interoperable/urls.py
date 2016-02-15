#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('api_interoperable.views',
    url(r'^list-depor/$', 'deportista_list', name='get_depor'),

)
urlpatterns = format_suffix_patterns(urlpatterns)