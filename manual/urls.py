from django.conf.urls import patterns, include, url

urlpatterns = patterns('manual.views',
    url(r'^nueva-entrada$', 'nueva_entrada', name='nueva_entrada_manual'),
    url(r'^ver-articulo$', 'ver_articulo', name='ver_articulo_manual'),
)