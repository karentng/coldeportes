from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from snd.views.dirigentes import *

"""
Autor: Cristian Ríos
Conjunto de formularios pasados al wizard según el paso actual del wizard
"""

FORMS = [
    ("Identificacion", DirigenteForm),
    ("Funciones", DirigenteFuncionesForm),
]

Dirigente_wizard = DirigenteWizard.as_view(FORMS, url_name='dirigentes_crear_step', done_step_name="Finalizado")

urlpatterns = patterns('snd.views.dirigentes',
    url(r'^nuevo/(?P<step> +)$', Dirigente_wizard, name='dirigentes_crear_step'),
    url(r'^nuevo$', Dirigente_wizard, name='dirigentes_crear'),
    url(r'^listar$', 'listarDirigentes', name='dirigentes_listar'),
)
