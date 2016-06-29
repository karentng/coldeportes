from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('registro_resultados.views.reportes',
    url(r'medalleria-genero$', 'medalleria_genero', name='reporte_medalleria_genero'),
    url(r'tabla-medalleria$', 'tabla_medalleria', name='reporte_tabla_medalleria'),   

)