#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from reportes.utilities import puede_ver_reporte
from coldeportes.utilities import required

urlpatterns = patterns('reportes.views.publico',
	url(r'^$', 'tipos', name='reportes_publico_tipos'),
    url(r'^tipos$', 'tipos', name='reportes_publico_tipos'),
    #url(r'centros-acondicionamiento/', include('reportes.urls.caf')),
    #url(r'depor/', include('reportes.urls.deportistas')),
    #url(r'personal-apoyo/', include('reportes.urls.personal_apoyo')),
    #url(r'escenario/', include('reportes.urls.escenarios')),
    #url(r'dirigentes/', include('reportes.urls.dirigentes')),
    #url(r'escuelas/', include('reportes.urls.escuelas')),
)


urlpatterns += required(
    puede_ver_reporte('escenario'),
    patterns('',
        url(r'^escenario/', include('reportes.urls.escenarios')), #urls de cafs
    ),

)

urlpatterns += required(
    puede_ver_reporte('centroacondicionamiento'),
    patterns('',
        url(r'^centros-acondicionamiento/', include('reportes.urls.caf')), #urls de cafs
    ),

)

urlpatterns += required(
    puede_ver_reporte('dirigente'),
    patterns('',
        url(r'dirigentes/', include('reportes.urls.dirigentes')),
    ),

)

urlpatterns += required(
    puede_ver_reporte('escueladeportiva'),
    patterns('',
        url(r'escuelas/', include('reportes.urls.escuelas')),
    ),

)

urlpatterns += required(
    puede_ver_reporte('personalapoyo'),
    patterns('',
        url(r'personal-apoyo/', include('reportes.urls.personal_apoyo')),
    ),

)

urlpatterns += required(
    puede_ver_reporte('deportista'),
    patterns('',
        url(r'depor/', include('reportes.urls.deportistas')),
    ),

)

