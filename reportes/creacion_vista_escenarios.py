from django.db import connection

def crear_vista_reportes_tenant_escenario(entidad):
    sql_tenant = ("""create or replace view reportes_escenarioview as 
    select  E.id, E.nombre,
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
    from %s.snd_escenario E 
    LEFT join %s.snd_caracterizacionescenario CE on CE.escenario_id=E.id 
    LEFT join %s.snd_caracterizacionescenario_caracteristicas CEC on CEC.caracterizacionescenario_id=E.id 
    LEFT join %s.snd_caracterizacionescenario_tipo_superficie_juego CTJ on CTJ.caracterizacionescenario_id=E.id 
    LEFT join %s.snd_caracterizacionescenario_tipo_disciplinas CTD on CTD.caracterizacionescenario_id=E.id 
    LEFT join %s.snd_caracterizacionescenario_clase_uso CCU on CCU.caracterizacionescenario_id=E.id 
    LEFT join %s.snd_contacto C on C.escenario_id=E.id 
    LEFT join %s.snd_horariodisponibilidad H on H.escenario_id=E.id
    LEFT join %s.snd_horariodisponibilidad_dias HD on HD.horariodisponibilidad_id=H.id
    LEFT join %s.snd_foto F on F.escenario_id=E.id
    LEFT join %s.snd_video V on V.escenario_id=E.id
    LEFT join %s.snd_datohistorico DH on DH.escenario_id=E.id
    LEFT join %s.snd_mantenimiento M on M.escenario_id=E.id;
    """)%(entidad,entidad,entidad,entidad,entidad,entidad,entidad,entidad,entidad,entidad,entidad,entidad,entidad,)

    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql_tenant)
    r=connection.commit()
    return r


def generar_vista_escenario():
    from django.db import connection

    sql = """
        CREATE OR REPLACE VIEW public.reportes_reporteescenarioview AS
    """

    from entidades.models import Entidad
    entidades = Entidad.objects.exclude(schema_name='public').order_by('id')#.values_list('schema_name', flat=True)
    primero = entidades[1]

    for entidad in entidades:
        #if entidad == 'public':
        #    pass
        schema =  entidad.schema_name
        connection.set_tenant(entidad) 
        crear_vista_reportes_tenant_escenario(schema)

        aux = ("""
            SELECT
                select *
            FROM
            %s.reportes_escenarioview E
        """)%(entidad)

        if primero == entidad:
            sql = ("%s %s")%(sql, aux)
        else:
            sql = ("%s UNION %s")%(sql, aux)
        
    sql = ("%s %s")%(sql, ";")
    connection.set_tenant('public')

    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql)
    r=connection.commit()
    return r