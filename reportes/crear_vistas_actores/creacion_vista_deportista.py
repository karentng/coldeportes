from django.db import connection

def crear_vista_reportes_tenant_deportista():
    sql_tenant = """
    CREATE MATERIALIZED view reportes_tenantdeportistaview AS
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
    snd_deportista DE
    LEFT JOIN snd_deportista_nacionalidad NAL ON NAL.deportista_id = DE.id
    LEFT JOIN snd_deportista_disciplinas DIS ON DIS.deportista_id = DE.id
    LEFT JOIN snd_historialdeportivo HD ON HD.deportista_id = DE.id
    LEFT JOIN snd_informacionacademica IA ON IA.deportista_id = DE.id
    LEFT JOIN snd_informacionadicional ID ON ID.deportista_id = DE.id
    LEFT JOIN snd_historiallesiones HL ON HL.deportista_id = DE.id
    LEFT JOIN snd_historialdoping IFD ON IFD.deportista_id = DE.id;
    """

    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql_tenant)
    r=connection.commit()
    return r

def generar_vista_deportista(nuevo_tenant=None):
    from django.db import connection

    #Definiendo tenant actual
    tenant_actual = connection.tenant

    sql = """
        CREATE MATERIALIZED VIEW public.entidades_publicdeportistaview AS
    """

    from entidades.models import Entidad
    entidades = Entidad.objects.exclude(schema_name='public').order_by('id')
    primero = entidades[0]

    if nuevo_tenant:
        connection.set_tenant(nuevo_tenant)
        crear_vista_reportes_tenant_deportista()

    for entidad in entidades:
        connection.set_tenant(entidad)
        if not nuevo_tenant:
            crear_vista_reportes_tenant_deportista()

        aux = ("""
                SELECT * FROM %s.reportes_tenantdeportistaview E
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
