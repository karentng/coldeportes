from django.conf.urls import patterns, include, url

urlpatterns = patterns('gestion_usuarios.views',
	url(r'^crear$', 'crear', name="usuarios_crear"),
	url(r'^modificar/(\d+)$', 'modificar', name="usuarios_modificar"),
	url(r'^password/(\d+)$', 'password', name="usuarios_password"),
	url(r'^lista$', 'lista', name="usuarios_lista"),
)