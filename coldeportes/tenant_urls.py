from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from coldeportes.utilities import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'gestion_usuarios.views.inicio', name='inicio'),
    url(r'^inicio$','gestion_usuarios.views.inicio_tenant',name='inicio_tenant'), #Url para redireccion al index del tenant
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'login'}, name='logout'),
    url(r'^cambiar-pass/$', 'django.contrib.auth.views.password_change', {'template_name':'cambiar-pass.html', 'post_change_redirect':'inicio'}, name='cambiar_pass'),

    url(r'^gestion-usuarios/', include('gestion_usuarios.urls')),
    url(r'^transferencias/',include('transferencias.urls')),#urls del modulo de transferencias
    url(r'^directorio/',include('directorio.entidad_urls')),#urls del modulo de directorio perfil entidad
    url(r'^directorio-publico/',include('directorio.publico_urls')),#urls del modulo de directorio publico
    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += required(
    tenant_actor('centros'),
    patterns('',
        url(r'^caf/', include('snd.urls.caf')), #urls de cafs
    ),
    
)

urlpatterns += required(
    tenant_actor('escenarios'),
    patterns('',
        url(r'^escenarios/', include('snd.urls.escenarios')), #urls de escenarios
    ),

)
    

urlpatterns += required(
    tenant_actor('cajas'),
    patterns('',
        url(r'^ccf/', include('snd.urls.cajas_compensacion')), #urls de cajas
    )
    
)

urlpatterns += required(
    tenant_actor('dirigentes'),
    patterns('',
        url(r'^dirigentes/', include('snd.urls.dirigentes')), #urls de dirigentes
    )
    
)

urlpatterns += required(
    tenant_actor('deportistas'),
    patterns('',
        url(r'^deportistas/', include('snd.urls.deportistas')), #urls de deportistas
    )
    
)

urlpatterns += required(
    tenant_actor('personal_apoyo'),
    patterns('',
        url(r'^personal-apoyo/', include('snd.urls.personal_apoyo')), #urls de personal de apoyo
    )
    
)