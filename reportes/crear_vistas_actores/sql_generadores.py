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

def seleccion_datos_escenarios(tenant=''):
    if tenant != '':
        tenant = ("%s.")%(tenant)
    return ("""
    SELECT  E.id, E.nombre,
            E.direccion, E.latitud,         
            E.longitud, E.altura,       
            E.ciudad_id, E.comuna,      
            E.barrio, E.estrato,        
            E.nombre_administrador,
            E.division_territorial,
            E.descripcion as descripcion_escenario,
            E.fecha_creacion,         
            E.entidad_id, E.estado,
            E.fecha_creacion as fecha_creacion_escenario,

            CE.metros_construidos,
            CE.tipo_escenario_id,
            CE.clase_acceso,
            CE.estado_fisico,
            CE.capacidad_espectadores,
            CE.espectadores_habituales,
            CE.tipo_propietario,
            CE.descripcion as descripcion_caracterizacion,
            CE.fecha_creacion as fecha_creacion_caracterizacion_escenario,

            CEC.caracteristicaescenario_id as caracteristicas_id,
            CTJ.tiposuperficie_id,
            CTD.tipodisciplinadeportiva_id,
            CCU.tipousoescenario_id,

            C.nombre as nombre_contacto,        
            C.telefono as telefono_contacto,        
            C.email as email_contacto,      
            C.descripcion as descripcion_contacto,
            C.fecha_creacion as fecha_creacion_contacto,

            H.id as horario_id,      
            H.hora_inicio,      
            H.hora_fin,                 
            H.descripcion as descripcion_horario,  
            H.fecha_creacion as fecha_creacion_horario_disponibilidad,     
            HD.dias_id,    

            F.foto,
            F.titulo,
            F.descripcion as descripcion_foto,
            F.fecha_creacion as fecha_creacion_foto,

            V.url,
            V.descripcion as descripcion_video,
            V.fecha_creacion as fecha_creacion_video,

            M.fecha_ultimo_mantenimiento,
            M.descripcion_ultimo_mantenimiento,
            M.periodicidad,
            M.razones_no_mantenimiento,
            M.tiene_planos,
            M.fecha_creacion as fecha_creacion_mantenimiento,

            DH.fecha_inicio,
            DH.fecha_fin,
            DH.descripcion as descripcion_dato_historico,
            DH.fecha_creacion as fecha_creacion_dato_historico
    FROM %ssnd_escenario E 
    LEFT join %ssnd_caracterizacionescenario CE on CE.escenario_id=E.id 
    LEFT join %ssnd_caracterizacionescenario_caracteristicas CEC on CEC.caracterizacionescenario_id=E.id 
    LEFT join %ssnd_caracterizacionescenario_tipo_superficie_juego CTJ on CTJ.caracterizacionescenario_id=E.id 
    LEFT join %ssnd_caracterizacionescenario_tipo_disciplinas CTD on CTD.caracterizacionescenario_id=E.id 
    LEFT join %ssnd_caracterizacionescenario_clase_uso CCU on CCU.caracterizacionescenario_id=E.id 
    LEFT join %ssnd_contacto C on C.escenario_id=E.id 
    LEFT join %ssnd_horariodisponibilidad H on H.escenario_id=E.id
    LEFT join %ssnd_horariodisponibilidad_dias HD on HD.horariodisponibilidad_id=H.id
    LEFT join %ssnd_foto F on F.escenario_id=E.id
    LEFT join %ssnd_video V on V.escenario_id=E.id
    LEFT join %ssnd_datohistorico DH on DH.escenario_id=E.id
    LEFT join %ssnd_mantenimiento M on M.escenario_id=E.id
    """)%(tenant, tenant, tenant, tenant, tenant, tenant, tenant, tenant, tenant, tenant, tenant, tenant, tenant)


def seleccion_datos_personal_apoyo(tenant=''):
    if tenant != '':
        tenant = ("%s.")%(tenant)
    return (
        """
        SELECT
            PA.id, PA.actividad,
            PA.genero, PA.tipo_id,
            PA.fecha_nacimiento, NAL.nacionalidad_id,
            PA.ciudad_id, PA.etnia,
            PA.lgtbi, PA.fecha_creacion,
            PA.estado,
            FD.nivel as nivel_formacion, FD.estado as estado_formacion,
            FD.fecha_finalizacion as ano_final_formacion, FD.fecha_creacion as creacion_formacion
        FROM
        %ssnd_personalapoyo PA
        LEFT JOIN %ssnd_formaciondeportiva FD ON FD.personal_apoyo_id = PA.id
        LEFT JOIN %ssnd_personalapoyo_nacionalidad NAL ON NAL.personalapoyo_id = PA.id
        """)%(tenant,tenant,tenant)


def seleccion_datos_deportistas(tenant=''):
    if tenant != '':
        tenant = ("%s.")%(tenant)
    return (
        """
        SELECT
            DE.id, DE.genero,
            DE.ciudad_residencia_id,DIS.tipodisciplinadeportiva_id,
            DE.fecha_nacimiento,DE.fecha_creacion,
            DE.lgtbi,DE.etnia,
            NAL.nacionalidad_id,DE.estado,
            HD.tipo as tipo_participacion, HD.estado as estado_participacion ,
            IA.nivel as nivel_formacion, IA.estado as estado_formacion,
            ID.usa_centros_biomedicos,ID.es_beneficiario_programa_apoyo,
            HL.tipo_lesion,HL.periodo_rehabilitacion, IFD.fecha as fecha_doping
        FROM
        %ssnd_deportista DE
        LEFT JOIN %ssnd_deportista_nacionalidad NAL ON NAL.deportista_id = DE.id
        LEFT JOIN %ssnd_deportista_disciplinas DIS ON DIS.deportista_id = DE.id
        LEFT JOIN %ssnd_historialdeportivo HD ON HD.deportista_id = DE.id
        LEFT JOIN %ssnd_informacionacademica IA ON IA.deportista_id = DE.id
        LEFT JOIN %ssnd_informacionadicional ID ON ID.deportista_id = DE.id
        LEFT JOIN %ssnd_historiallesiones HL ON HL.deportista_id = DE.id
        LEFT JOIN %ssnd_historialdoping IFD ON IFD.deportista_id = DE.id
        """)%(tenant,tenant,tenant,tenant,tenant,tenant,tenant,tenant)

COMANDOS_GENERADORES_DE_VISTAS_ACTORES = [
    #[
    #   Funcion que genera el comando de seleccion de datos,
    #   Nombre de la vista (tenant),
    #   Nombre vista materializada (public)
    #]
    [
        seleccion_datos_cafs,
        "reportes_tenantcafview",
        "public.entidades_publiccafview",
    ],
    [
        seleccion_datos_escenarios,
        "reportes_tenantescenarioview",
        "public.entidades_publicescenarioview",
    ],
    [
        seleccion_datos_personal_apoyo,
        "reportes_tenantpersonalapoyoview",
        "public.entidades_publicpersonalapoyoview"
    ],
    [
        seleccion_datos_deportistas,
        "reportes_tenantdeportistaview",
        "public.entidades_publicdeportistaview"
    ]
]