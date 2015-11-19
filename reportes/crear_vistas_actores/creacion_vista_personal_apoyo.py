from django.db import connection

def crear_vista_reportes_tenant_personal_apoyo():
    sql_tenant = """
    CREATE OR REPLACE view reportes_tenantpersonalapoyoview AS
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
    snd_personalapoyo PA
    LEFT JOIN snd_formaciondeportiva FD ON FD.personal_apoyo_id = PA.id
    LEFT JOIN snd_personalapoyo_nacionalidad NAL ON NAL.personalapoyo_id = PA.id;
    """

    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql_tenant)
    r=connection.commit()
    return r


def generar_vista_personal_apoyo(nuevo_tenant=None):
    from django.db import connection

    #Definiendo tenant actual
    tenant_actual = connection.tenant

    sql = """
        CREATE OR REPLACE VIEW public.entidades_publicpersonalapoyoview AS
    """

    from entidades.models import Entidad
    entidades = Entidad.objects.exclude(schema_name='public').order_by('id')
    primero = entidades[0]

    if nuevo_tenant:
        connection.set_tenant(nuevo_tenant)
        crear_vista_reportes_tenant_personal_apoyo()

    for entidad in entidades:
        connection.set_tenant(entidad)
        if not nuevo_tenant:
            crear_vista_reportes_tenant_personal_apoyo()

        aux = ("""
                SELECT * FROM %s.reportes_tenantpersonalapoyoview E
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