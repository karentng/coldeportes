from django.db import connection

def crear_vista_reportes_tenant_escenario():
    sql_tenant = """
    CREATE OR REPLACE view reportes_escenarioview AS 
    SELECT  E.id, E.nombre,
            E.direccion, E.latitud,         
            E.longitud, E.altura,       
            E.ciudad_id, E.comuna,      
            E.barrio, E.estrato,        
            E.nombre_administrador,
            E.division_territorial,
            E.descripcion as descripcion_escenario,
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
    FROM snd_escenario E 
    LEFT join snd_caracterizacionescenario CE on CE.escenario_id=E.id 
    LEFT join snd_caracterizacionescenario_caracteristicas CEC on CEC.caracterizacionescenario_id=E.id 
    LEFT join snd_caracterizacionescenario_tipo_superficie_juego CTJ on CTJ.caracterizacionescenario_id=E.id 
    LEFT join snd_caracterizacionescenario_tipo_disciplinas CTD on CTD.caracterizacionescenario_id=E.id 
    LEFT join snd_caracterizacionescenario_clase_uso CCU on CCU.caracterizacionescenario_id=E.id 
    LEFT join snd_contacto C on C.escenario_id=E.id 
    LEFT join snd_horariodisponibilidad H on H.escenario_id=E.id
    LEFT join snd_horariodisponibilidad_dias HD on HD.horariodisponibilidad_id=H.id
    LEFT join snd_foto F on F.escenario_id=E.id
    LEFT join snd_video V on V.escenario_id=E.id
    LEFT join snd_datohistorico DH on DH.escenario_id=E.id
    LEFT join snd_mantenimiento M on M.escenario_id=E.id;
    """

    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql_tenant)
    r=connection.commit()
    return r


def generar_vista_escenario(nuevo_tenant=None):
    from django.db import connection

    #Definiendo tenant actual
    tenant_actual = connection.tenant

    sql = """
        CREATE OR REPLACE VIEW public.entidades_publicescenarioview AS
    """

    from entidades.models import Entidad
    entidades = Entidad.objects.exclude(schema_name='public').order_by('id')
    primero = entidades[0]

    if nuevo_tenant:
        connection.set_tenant(nuevo_tenant)
        crear_vista_reportes_tenant_escenario()

    for entidad in entidades:
        connection.set_tenant(entidad)
        if not nuevo_tenant:
            crear_vista_reportes_tenant_escenario()

        aux = ("""
                SELECT * FROM %s.reportes_tenantescenarioview E
              """)%(entidad.schema_name)

        if primero == entidad:
            sql = ("%s %s")%(sql, aux)
        else:
            sql += (" UNION %s")%(aux)


    public = Entidad.objects.get(schema_name='public')
    connection.set_tenant(public)
        
    sql = ("%s %s")%(sql, ";")
    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql)
    r=connection.commit()

    connection.set_tenant(tenant_actual)

        
