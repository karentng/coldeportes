#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from api_interoperable import views

router_deportistas = DefaultRouter()
router_deportistas.register(r'basico', views.DeportistaViewSet)
router_deportistas.register(r'corporal', views.ComposcionCorporalViewSet)
router_deportistas.register(r'deportivo', views.HistorialDeportivolViewSet)
router_deportistas.register(r'academico', views.InformacionAcademicaViewSet)
router_deportistas.register(r'adicional', views.InformacionAdicionalViewSet)
router_deportistas.register(r'lesiones', views.HistorialLesionesViewSet)

urlpatterns = [
    url(r'^deportistas/', include(router_deportistas.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]