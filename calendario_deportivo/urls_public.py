from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('calendario_deportivo.views',
    url(r'^ver-calendario$', 'cargar_calendario', name='cargar_calendario_nacional'),
    url(r'^listar-todos$', 'listar_todos_calendario', name='listar_todos_calendario'),
    url(r'^listar-pendientes$', 'listar_pendientes_calendario', name='listar_aprobar_calendario'),
    url(r'^ver-evento/(\d+)', 'ver_evento_nacional', name='ver_evento_nacional'),
    url(r'^aprobar/(\d+)', 'aprobar_evento', name='aprobar_evento_nacional'),
    url(r'^reprobar/(\d+)', 'reprobar_evento', name='reprobar_evento_nacional'),


)
