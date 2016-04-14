def seleccion_datos_cafs(tenant=''):
    if tenant != '':
        tenant = ("%s.")%(tenant)
    return ("""
    SELECT
        CAF.id, CAF.nombre, CAF.telefono,
        CAF.direccion, CAF.ciudad_id,
        CAF.comuna, CAF.estrato,
        CAF.latitud, CAF.longitud,
        CAF.altura, CAF.estado,
        CAF.email, CAF.web, CAF.telefono as telefono_contacto,
        CAF.entidad_id, CAF.fecha_creacion,
        CAF.barrio, CAF.nombre_administrador,
        CLASE.nombre as nombre_clase, SERVICIO.nombre as nombre_servicio,
        F.foto
    FROM
    %ssnd_centroacondicionamiento CAF
    LEFT JOIN %ssnd_centroacondicionamiento_clases CLASES ON CLASES.centroacondicionamiento_id = CAF.id
    LEFT JOIN public.entidades_caclase CLASE ON CLASE.id = CLASES.caclase_id
    LEFT JOIN %ssnd_centroacondicionamiento_servicios SERVICIOS ON SERVICIOS.centroacondicionamiento_id = CAF.id
    LEFT JOIN public.entidades_caservicio SERVICIO ON SERVICIO.id = SERVICIOS.caservicio_id
    LEFT JOIN %ssnd_cafoto F on F.centro_id=CAF.id
    """)%(tenant, tenant, tenant, tenant)

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
            CE.espectadores_habituales,
            CE.tipo_propietario,
            CE.descripcion as descripcion_caracterizacion,
            CE.fecha_creacion as fecha_creacion_caracterizacion_escenario,
            CE.capacidad_espectadores,

            CEC.caracteristicaescenario_id,
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
            F.descripcion_foto,
            F.fecha_creacion as fecha_creacion_foto,

            V.url,
            V.descripcion_video,
            V.fecha_creacion as fecha_creacion_video,

            M.fecha_ultimo_mantenimiento,
            M.descripcion_ultimo_mantenimiento,
            M.periodicidad,
            M.inversionista,
            M.convenio,
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
            PA.genero, PA.tipo_id, PA.foto,
            PA.nombres, PA.apellidos, PA.identificacion,
            PA.fecha_nacimiento, NAL.nacionalidad_id,            
            PA.telefono_fijo as telefono_contacto,
            PA.ciudad_id, PA.etnia, PA.telefono_celular,
            PA.lgtbi, PA.fecha_creacion,
            PA.estado, PA.entidad_id, PA.correo_electronico, 
            FD.nivel as nivel_formacion, FD.estado as estado_formacion,
            FD.fecha_finalizacion
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
            DE.lgtbi,DE.etnia, DE.barrio, DE.comuna,
            DE.email, DE.telefono as telefono_contacto,
            DE.direccion, DE.foto, DE.identificacion,
            DE.nombres, DE.apellidos, DE.entidad_id,
            NAL.nacionalidad_id,DE.estado,
            HD.tipo as tipo_participacion, HD.estado as estado_participacion ,
            HD.fecha_inicial as fecha_participacion,
            IA.nivel as nivel_formacion, IA.estado as estado_formacion,
            IA.fecha_finalizacion,
            ID.usa_centros_biomedicos,ID.es_beneficiario_programa_apoyo,
            HL.tipo_lesion,HL.periodo_rehabilitacion, HL.fecha_lesion,
            HL.segmento_corporal
        FROM
        %ssnd_deportista DE
        LEFT JOIN %ssnd_deportista_nacionalidad NAL ON NAL.deportista_id = DE.id
        LEFT JOIN %ssnd_deportista_disciplinas DIS ON DIS.deportista_id = DE.id
        LEFT JOIN %ssnd_historialdeportivo HD ON HD.deportista_id = DE.id
        LEFT JOIN %ssnd_informacionacademica IA ON IA.deportista_id = DE.id
        LEFT JOIN %ssnd_informacionadicional ID ON ID.deportista_id = DE.id
        LEFT JOIN %ssnd_historiallesiones HL ON HL.deportista_id = DE.id
        """)%(tenant,tenant,tenant,tenant,tenant,tenant,tenant)

def seleccion_datos_dirigentes(tenant=''):
    if tenant != '':
        tenant = ("%s.")%(tenant)
    return (
        """
        SELECT
            DIR.id, NAL.nacionalidad_id,
            DIR.nombres, DIR.apellidos,
            DIR.foto, DIR.identificacion,
            DIR.entidad_id, DIR.fecha_creacion,
            DIR.genero, DIR.telefono_fijo as telefono_contacto,
            DIR.estado, DIR.ciudad_residencia_id AS ciudad_id,
            C.cargo, DIR.email
        FROM
        {0}snd_dirigente DIR
        LEFT JOIN {0}snd_dirigente_nacionalidad NAL ON NAL.dirigente_id = DIR.id
        LEFT join (SELECT DIC.id, DIC.dirigente_id, DIC.nombre as cargo, max(fecha_posesion) as fecha_posesion_cargo FROM snd_dirigentecargo as DIC group by DIC.id) C on C.dirigente_id=DIR.id
        """.format(tenant))

def seleccion_datos_escuelas(tenant=''):
    if tenant != '':
        tenant = ("%s.")%(tenant)
    return (
        """
        SELECT
            ESCUELA.id, ESCUELA.estrato, ESCUELA.nombre, ESCUELA.tipo_sede,
            ESCUELA.estado, ESCUELA.ciudad_id, ESCUELA.telefono_fijo,
            ESCUELA.email, ESCUELA.web,
            ESCUELA.entidad_id, ESCUELA.fecha_creacion,
            SERVICIO.nombre as nombre_servicio
        FROM
        {0}snd_escueladeportiva ESCUELA
        LEFT JOIN {0}snd_escueladeportiva_servicios SERVICIOS ON SERVICIOS.escueladeportiva_id = ESCUELA.id
        LEFT JOIN public.entidades_escueladeportivaservicio SERVICIO ON SERVICIO.id = SERVICIOS.escueladeportivaservicio_id
    """.format(tenant))

def seleccion_datos_cajas(tenant=''):
    if tenant != '':
        tenant = ("%s.")%(tenant)
    return (
        """
        SELECT
            CAJA.id, CAJA.nombre,
            CAJA.estado, CAJA.ciudad_id,
            CAJA.email, CAJA.clasificacion,
            CAJA.entidad_id, CAJA.foto,
            CAJA.telefono_contacto, 
            CAJA.nombre_contacto,
            SERVICIO.categoria,
            SERVICIO.descripcion
        FROM
        {0}snd_cajacompensacion CAJA
        LEFT JOIN {0}snd_cajacompensacion_servicios SERVICIOS ON SERVICIOS.cajacompensacion_id = CAJA.id
        LEFT JOIN public.entidades_tiposerviciocajacompensacion SERVICIO ON SERVICIO.id = SERVICIOS.cajacompensacion_id
    """.format(tenant))

COMANDOS_GENERADORES_DE_VISTAS_ACTORES = [
    #[
    #   Funcion que genera el comando de seleccion de datos,
    #   Nombre de la vista (tenant),
    #   Nombre vista materializada (public)
    #]
    [
        seleccion_datos_cafs,
        "reportes_tenantcafview",
        "public.entidades_publiccafview"
    ],
    [
        seleccion_datos_escenarios,
        "reportes_tenantescenarioview",
        "public.entidades_publicescenarioview"
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
    ],
    [
        seleccion_datos_dirigentes,
        "reportes_tenantdirigenteview",
        "public.entidades_publicdirigenteview"
    ],
    [
        seleccion_datos_escuelas,
        "reportes_tenantescuelaview",
        "public.entidades_publicescuelaview"
    ],
    [
        seleccion_datos_cajas,
        "reportes_tenantcajasview",
        "public.entidades_publiccajasview"
    ],
]