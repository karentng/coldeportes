#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from api_interoperable import views

urlpatterns = patterns('api_interoperable.views',
    #url(r'^$', views.api_root, name='rest_root'),
    url(r'^deportistas/$', views.DeportistasList.as_view()),
    url(r'^deportistas/(?P<pk>[0-9]+)$', views.DeportistaDetail.as_view()),
    url(r'^deportistas/corporal$', views.ComposcionCorporalList.as_view()),
    url(r'^deportistas/corporal/(?P<pk>[0-9]+)$', views.ComposcionCorporalDetail.as_view()),
    url(r'^deportistas/historialdeportivo', views.HistorialDeportivolList.as_view()),
    url(r'^deportistas/historialdeportivo/(?P<pk>[0-9]+)$', views.HistorialDeportivoDetail.as_view()),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),

)
urlpatterns = format_suffix_patterns(urlpatterns)