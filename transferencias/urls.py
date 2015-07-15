from django.conf.urls import patterns, include, url

urlpatterns = patterns('transferencias.views',
    url(r'^generar/(\d+)/(\d+)/(\d+)$', 'generar_transferencia', name='generar_transferencia'),
    url(r'^procesar/(\d+)/(\d+)/(\d+)$', 'procesar_transferencia', name='procesar_transferencia'),

)
