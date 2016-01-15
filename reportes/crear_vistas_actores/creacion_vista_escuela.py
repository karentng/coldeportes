from django.db import connection

def eliminar_vista_reportes_public_escuela():
    sql_tenant = """
        DROP MATERIALIZED VIEW IF EXISTS public.entidades_publicescuelaview;
    """

    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql_tenant)
    r=connection.commit()
    return r

def crear_vista_reportes_tenant_escuela(nuevo_tenant):
    sql_tenant = """
    CREATE OR REPLACE VIEW reportes_tenantescuelaview AS 
    SELECT
        ESCUELA.id, ESCUELA.estrato,
        ESCUELA.estado, ESCUELA.ciudad_id,
        ESCUELA.entidad_id, ESCUELA.fecha_creacion,
        SERVICIO.nombre as nombre_servicio
    FROM
    snd_escueladeportiva ESCUELA
    LEFT JOIN snd_escueladeportiva_servicios SERVICIOS ON SERVICIOS.escueladeportiva_id = ESCUELA.id
    LEFT JOIN public.entidades_escueladeportivaservicio SERVICIO ON SERVICIO.id = SERVICIOS.escueladeportivaservicio_id;
    """

    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql_tenant)
    r=connection.commit()
    return r


def generar_vista_escuela(nuevo_tenant=None):
    from django.db import connection

    #Definiendo tenant actual
    tenant_actual = connection.tenant

    sql = """
        CREATE MATERIALIZED VIEW public.entidades_publicescuelaview AS
    """

    from entidades.models import Entidad
    entidades = Entidad.objects.exclude(schema_name='public').order_by('id')
    primero = entidades[0]

    if nuevo_tenant:
        connection.set_tenant(nuevo_tenant)
        crear_vista_reportes_tenant_escuela()

    for entidad in entidades:
        connection.set_tenant(entidad)
        if not nuevo_tenant:
            crear_vista_reportes_tenant_escuela(nuevo_tenant)

        aux = ("""
                SELECT * FROM %s.reportes_tenantescuelaview E
              """)%(entidad.schema_name)

        if primero == entidad:
            sql = ("%s %s")%(sql, aux)
        else:
            sql += (" UNION %s")%(aux)


    public = Entidad.objects.get(schema_name='public')
    connection.set_tenant(public)
    
    eliminar_vista_reportes_public_escuela()

    sql = ("%s %s")%(sql, ";")
    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql)
    r=connection.commit()

    connection.set_tenant(tenant_actual)