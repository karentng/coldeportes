from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'gestion_usuarios.views.inicio', name='inicio'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'login'}, name='logout'),


    url(r'^gestion-usuarios/', include('gestion_usuarios.urls')),
    url(r'^escenarios/', include('snd.urls.escenarios')), #urls de escenarios
    url(r'^caf/', include('snd.urls.caf')), #urls de escenarios
)