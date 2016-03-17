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
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'inicio'}, name='logout'),
    url(r'^cambiar-pass/$', 'django.contrib.auth.views.password_change', {'template_name':'cambiar-pass.html', 'post_change_redirect':'inicio'}, name='cambiar_pass'),

    url(r'^gestion-usuarios/', include('gestion_usuarios.urls')),
    url(r'^transferencias/',include('transferencias.urls')),#urls del modulo de transferencias
    url(r'^directorio/',include('directorio.entidad_urls')),#urls del modulo de directorio perfil entidad
    url(r'^directorio-publico/',include('directorio.publico_urls')),#urls del modulo de directorio publico
    url(r'^normograma/',include('normograma.urls')),#urls del modulo de normograma
    url(r'^clasificados/',include('publicidad.urls')),#urls del modulo de clasificados
    url(r'^noticias/',include('noticias.urls')),#urls del modulo de noticias
    #url(r'^casos-doping/', include('listados_doping.urls')), #urls de listados de doping

    #url(r'^selecciones/', include('snd.urls.selecciones')), #urls de selecciones
    url(r'^cargado-datos/', include('snd.urls.cargado_datos')),
    url(r'^manual/',include('manual.urls')),
    url(r'^reportes/', include('reportes.urls.publico')),
    url(r'^solicitudes-escenarios/solicitud/', include('solicitudes_escenarios.solicitud.urls')),
    url(r'^solicitudes-escenarios/respuesta/', include('solicitudes_escenarios.respuesta.urls')),
    url(r'^gestion-socios$', 'entidades.views.mostrar_gestion_socios', name='gestion_socios'),
    url(r'^desactivar-socio/(\d+)$', 'entidades.views.desactivar_socio', name='desactivar_socio'),
    url(r'^editar-socio/(\d+)$', 'entidades.views.editar_socio', name='editar_socio'),

    #GESTION PLANES DE COSTOS
    url(r'^planes$', 'entidades.views.crear_plan_de_costo', name='crear_plan_de_costo'),
    url(r'^cambiar/(\d+)$', 'entidades.views.cambiar_estado_plan_costo', name='cambiar_estado_plan_costo'),
    url(r'^editar/(\d+)$', 'entidades.views.editar_plan_de_costo', name='editar_plan_de_costo'),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += required(
    tenant_actor('seleccion'),
    patterns('',
        url(r'^selecciones/', include('snd.urls.selecciones')), #urls de cafs
    ),
)

urlpatterns += required(
    tenant_actor('centroacondicionamiento'),
    patterns('',
        url(r'^caf/', include('snd.urls.caf')), #urls de cafs
    ),
    
)

urlpatterns += required(
    tenant_actor('escenario'),
    patterns('',
        url(r'^escenarios/', include('snd.urls.escenarios')), #urls de escenarios
    ),

)
    

urlpatterns += required(
    tenant_actor('cajacompensacion'),
    patterns('',
        url(r'^ccf/', include('snd.urls.cajas_compensacion')), #urls de cajas
    )
    
)

urlpatterns += required(
    tenant_actor('dirigente'),
    patterns('',
        url(r'^dirigentes/', include('snd.urls.dirigentes')), #urls de dirigentes
    )
    
)

urlpatterns += required(
    tenant_actor('deportista'),
    patterns('',
        url(r'^deportistas/', include('snd.urls.deportistas')), #urls de deportistas
    )
    
)

urlpatterns += required(
    tenant_actor('personalapoyo'),
    patterns('',
        url(r'^personal-apoyo/', include('snd.urls.personal_apoyo')), #urls de personal de apoyo
    )
    
)

urlpatterns += required(
    tenant_actor('centrobiomedico'),
    patterns('',
        url(r'^centro-biomedico/', include('snd.urls.centro_biomedico')), #urls de centro biomédico
    )
    
)

urlpatterns += required(
    tenant_actor('escueladeportiva'),
    patterns('',
        url(r'^escuela-deportiva/', include('snd.urls.escuela_deportiva')), #urls de centro biomédico
    )
    
)

urlpatterns += required(
    tenant_actor('casodoping'),
    patterns('',
        url(r'^casos-doping/', include('listados_doping.urls')), #urls de listados de doping
    )
)