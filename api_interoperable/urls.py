#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from api_interoperable import views

urlpatterns = patterns('api_interoperable.views',
    url(r'^deportistas/$', views.DeportistasList.as_view(), name='get_depor'),
    url(r'^deportistas/(?P<pk>[0-9]+)$', views.DeportistaDetail.as_view(), name='get_depor_detail'),

    url(r'^auth/',include('rest_framework.urls',namespace='rest_framework')),

)
urlpatterns = format_suffix_patterns(urlpatterns)