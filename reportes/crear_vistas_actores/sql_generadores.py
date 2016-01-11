def seleccion_datos_cafs(tenant=''):
	if tenant != '':
		tenant = ("%s.")%(tenant)
	return ("""
	SELECT
        CAF.id, CAF.ciudad_id,
        CAF.comuna, CAF.estrato,
        CAF.latitud, CAF.longitud,
        CAF.altura, CAF.estado,
        CAF.entidad_id, CAF.fecha_creacion,
        CLASE.nombre as nombre_clase, SERVICIO.nombre as nombre_servicio
    FROM
    %ssnd_centroacondicionamiento CAF
    LEFT JOIN %ssnd_centroacondicionamiento_clases CLASES ON CLASES.centroacondicionamiento_id = CAF.id
    LEFT JOIN public.entidades_caclase CLASE ON CLASE.id = CLASES.caclase_id
    LEFT JOIN %ssnd_centroacondicionamiento_servicios SERVICIOS ON SERVICIOS.centroacondicionamiento_id = CAF.id
    LEFT JOIN public.entidades_caservicio SERVICIO ON SERVICIO.id = SERVICIOS.caservicio_id 
	""")%(tenant, tenant, tenant)

COMANDOS_GENERADORES_DE_VISTAS_ACTORES = [
	#[
	#	Funcion que genera el comando de seleccion de datos,
	#	Nombre de la vista (tenant),
	#	Nombre vista materializada (public)
	#]
	[
		seleccion_datos_cafs,
		"reportes_tenantcafview",
		"public.entidades_publiccafview",
	]
]