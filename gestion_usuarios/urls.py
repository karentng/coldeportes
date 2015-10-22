from django.conf.urls import patterns, include, url

urlpatterns = patterns('gestion_usuarios.views',
	url(r'^crear$', 'crear', name="usuarios_crear"),
	url(r'^modificar/(\d+)$', 'modificar', name="usuarios_modificar"),
	url(r'^password/(\d+)$', 'password', name="usuarios_password"),
	url(r'^listar$', 'lista', name="usuarios_lista"),
	url(r'^desactivar/(\d+)$', 'desactivar', name="usuarios_desactivar"),

	url(r'^grupo/crear$', 'grupos_crear', name="grupos_crear"),
	url(r'^grupo/modificar/(\d+)$', 'grupos_modificar', name="grupos_modificar"),
	url(r'^grupo/listar$', 'grupos_listar', name="grupos_listar"),

	url(r'^datos-basicos-entidad$', 'datos_basicos_entidad', name="datos_basicos_entidad"),
)