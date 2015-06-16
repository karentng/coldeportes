from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'gestion_usuarios.views.inicio', name='inicio'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'login'}, name='logout'),
    url(r'^cambiar-pass/$', 'django.contrib.auth.views.password_change', {'template_name':'cambiar-pass.html', 'post_change_redirect':'inicio'}, name='cambiar_pass'),

    url(r'^gestion-usuarios/', include('gestion_usuarios.urls')),
    url(r'^escenarios/', include('snd.urls.escenarios')), #urls de escenarios
    url(r'^caf/', include('snd.urls.caf')), #urls de cafs
    url(r'^deportistas/',include('snd.urls.deportistas')),#urls de deportistas
    url(r'^gestion_dirigentes/', include('snd.urls.dirigentes')), #urls de dirigentes
    url(r'^entrenadores/',include('snd.urls.entrenadores')),#urls de entrenadores
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)