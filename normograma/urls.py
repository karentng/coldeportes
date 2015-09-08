from django.conf.urls import patterns, include, url

urlpatterns = patterns('normograma.views',
    url(r'^registrar', 'registrar', name='normograma_registrar'),

)