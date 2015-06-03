#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.caf import *
from snd.formularios.caf  import *

"""
Autor: Andrés Serna
Conjunto de formularios pasados al wizard según el paso actual del wizard
"""


FORMS = [
    ("Identificación", CentroAcondicionamientoForm),
    ("Costos", CACostoUsoForm),
    ("Servicios", CAServiciosForm), 
    ("Otros", CAOtrosForm)
]

"""
Autor: Andrés Serna
Wizard de registro de CAF generado como vista
"""
CAF_wizard = CentroAcondicionamientoWizard.as_view(FORMS, url_name='nuevo_caf_step', done_step_name="Finalizado")

urlpatterns = patterns('snd.views.caf',
	url(r'^nuevo/(?P<step>.+)$', CAF_wizard, name='nuevo_caf_step'),
	url(r'^nuevo$', CAF_wizard, name='nuevo_caf'),

	url(r'^modificar/(\d+)$', 'modificar', name="modificar_caf"),
	url(r'^modificar/(\d+)/(\d+)$', 'modificar', name="modificar_caf"),
    
    url(r'^listar$', 'listarCAFS', name='listar_cafs'),    
    url(r'^desactivar/(\d+)$', 'desactivarCAF', name='desactivar_caf'),
)
