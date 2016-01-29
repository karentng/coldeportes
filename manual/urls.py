from django.conf.urls import patterns, include, url

urlpatterns = patterns('manual.views',
    url(r'^nueva-entrada$', 'nueva_entrada', name='nueva_entrada_manual'),
)