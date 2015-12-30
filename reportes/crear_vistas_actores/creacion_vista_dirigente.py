from django.db import connection

def eliminar_vista_reportes_public_dirigente():
    sql_tenant = """
        DROP MATERIALIZED VIEW IF EXISTS public.entidades_publicdirigenteview;
    """

    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql_tenant)
    r=connection.commit()
    return r

def crear_vista_reportes_tenant_dirigente(nuevo_tenant):
    sql_tenant = """
    CREATE OR REPLACE VIEW reportes_tenantdirigenteview AS 
    SELECT
        DIR.id, NAL.nacionalidad_id,
    FROM
    snd_dirigente DIR
    LEFT JOIN snd_dirigente_nacionalidad NAL ON NAL.dirigente_id = DIR.id;
    """

    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql_tenant)
    r=connection.commit()
    return r


def generar_vista_dirigente(nuevo_tenant=None):
    from django.db import connection

    #Definiendo tenant actual
    tenant_actual = connection.tenant

    sql = """
        CREATE MATERIALIZED VIEW public.entidades_publicdirigenteview AS
    """

    from entidades.models import Entidad
    entidades = Entidad.objects.exclude(schema_name='public').order_by('id')
    primero = entidades[0]

    if nuevo_tenant:
        connection.set_tenant(nuevo_tenant)
        crear_vista_reportes_tenant_caf()

    for entidad in entidades:
        connection.set_tenant(entidad)
        if not nuevo_tenant:
            crear_vista_reportes_tenant_dirigente(nuevo_tenant)

        aux = ("""
                SELECT * FROM %s.reportes_tenantdirigenteview E
              """)%(entidad.schema_name)

        if primero == entidad:
            sql = ("%s %s")%(sql, aux)
        else:
            sql += (" UNION %s")%(aux)


    public = Entidad.objects.get(schema_name='public')
    connection.set_tenant(public)
    
    eliminar_vista_reportes_public_dirigente()

    sql = ("%s %s")%(sql, ";")
    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql)
    r=connection.commit()

    connection.set_tenant(tenant_actual)