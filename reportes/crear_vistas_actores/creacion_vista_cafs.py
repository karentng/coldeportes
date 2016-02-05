from django.db import connection
from entidades.models import *

SQL_SELECCION_VISTA_TENANT_CAF = """
    SELECT
        CAF.id, CAF.ciudad_id,
        CAF.comuna, CAF.estrato,
        CAF.latitud, CAF.longitud,
        CAF.altura, CAF.estado,
        CAF.entidad_id, CAF.fecha_creacion,
        CLASE.nombre as nombre_clase, SERVICIO.nombre as nombre_servicio
    FROM
    snd_centroacondicionamiento CAF
    LEFT JOIN snd_centroacondicionamiento_clases CLASES ON CLASES.centroacondicionamiento_id = CAF.id
    LEFT JOIN public.entidades_caclase CLASE ON CLASE.id = CLASES.caclase_id
    LEFT JOIN snd_centroacondicionamiento_servicios SERVICIOS ON SERVICIOS.centroacondicionamiento_id = CAF.id
    LEFT JOIN public.entidades_caservicio SERVICIO ON SERVICIO.id = SERVICIOS.caservicio_id 
"""

SQL_CREACION_VISTA_TENANT_CAF = ("%s %s")%("CREATE OR REPLACE VIEW reportes_tenantcafview AS ", SQL_SELECCION_VISTA_TENANT_CAF)

def ejecutar_sql(sql):
    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql)
    r=connection.commit()
    return r

def generar_vista_caf(nuevo_tenant=None):
    if nuevo_tenant: # Solo se actualiza el padre del creado si existe
        generar_vista_caf_nuevo_tenant(nuevo_tenant)
        generar_vista_caf_padre_nuevo_tenant(nuevo_tenant.obtener_padre())
    else: # se deben actualizar todos
        # Clubes, Cafs, Escuelas, Cajas, Entes
        generar_vista_caf_independientes() 
        # Ligas, Federaciones, Comites
        generar_vista_caf_dependientes(Liga, (3, Club), "liga") # Ligas
        generar_vista_caf_dependientes(LigaParalimpica, (9, ClubParalimpico), "liga") # Ligas paralimpicas
        generar_vista_caf_dependientes(Federacion, (1, Liga), "federacion") # Federaciones
        generar_vista_caf_dependientes(FederacionParalimpica, (8, LigaParalimpica), "federacion") # Federaciones paralimpicas
        generar_vista_caf_dependientes(Comite, (2, Federacion), "comite") # Comite Olimpico
        generar_vista_caf_dependientes(Comite, (7, FederacionParalimpica), "comite") # Comite Paralimpico

    generar_vista_materializada_public()

def generar_vista_caf_padre_nuevo_tenant(padre):
    def obtener_parametros_generacion_vista(padre):
        tipo = padre.tipo
        if tipo == 1: # Liga
            return [(3, Club), "liga"]
        elif tipo == 2: #Federacion
            return [(1, Liga), "federacion"]
        elif tipo == 7: # Federacion Paralimpica
            return [(8, LigaParalimpica), "federacion"]
        elif tipo == 8: # Liga Paralimpica
            return [(9, ClubParalimpico), "liga"]
        elif tipo == 6:
            if padre.tipo_comite == 1: #Olimpico
                return [(2, Federacion), "comite"]
            else:
                return [(7, FederacionParalimpica), "comite"]
        return ("Hay algo malo con el tipo %s")%(tipo)

    if padre:
        parametros = obtener_parametros_generacion_vista(padre)
        connection.set_tenant(padre)
        kwargs = {
            "tipo": parametros[0][0],
            parametros[1]: padre
        }
        sql = ("%s %s")%("CREATE OR REPLACE VIEW reportes_tenantcafview AS", SQL_SELECCION_VISTA_TENANT_CAF)
        entidades_de_las_cuales_depende = parametros[0][1].objects.filter(**kwargs)
        for no_dependiente in entidades_de_las_cuales_depende:
            sql = ("%s UNION %s")%\
            (
                sql,
                ("SELECT * FROM %s.reportes_tenantcafview E")%(no_dependiente.schema_name)
            )
        ejecutar_sql(sql)

def generar_vista_caf_nuevo_tenant(nuevo_tenant):
    connection.set_tenant(nuevo_tenant)
    ejecutar_sql(SQL_CREACION_VISTA_TENANT_CAF)

def eliminar_vista_materializada_public():
    sql = "DROP MATERIALIZED VIEW IF EXISTS public.entidades_publiccafview;"
    ejecutar_sql(sql)

def obtener_entidades_del_tipo_de_modelo(modelo_tipo, modelo_dependiente):
    if modelo_tipo == Comite:
        if modelo_dependiente[1] == Federacion:
            return modelo_tipo.objects.filter(schema_name="coc")
        return modelo_tipo.objects.filter(schema_name="cpc")
    else:
        return modelo_tipo.objects.exclude(schema_name="public")

def generar_vista_materializada_public():
    todos_los_tenants = Entidad.objects.exclude(schema_name='public').order_by('id')
    primero = todos_los_tenants[0]
    todos_los_tenants = todos_los_tenants[1:]

    sql = ("%s %s")%\
    (
        "CREATE MATERIALIZED VIEW public.entidades_publiccafview AS",
        ("SELECT * FROM %s.reportes_tenantcafview E")%(primero.schema_name)
    )

    for tenant in todos_los_tenants:
        sql_tenant = ("SELECT * FROM %s.reportes_tenantcafview E")%(tenant.schema_name)
        sql = ("%s UNION %s")%(sql, sql_tenant)

    eliminar_vista_materializada_public()
    ejecutar_sql(sql)

def generar_vista_caf_independientes():
    entidades = Entidad.objects.filter(tipo__in=[3, 4, 5, 9, 10, 11])
    for entidad in entidades:
        connection.set_tenant(entidad)
        ejecutar_sql(SQL_CREACION_VISTA_TENANT_CAF)

def generar_vista_caf_dependientes(modelo_tipo, modelo_dependiente, campo_asociamiento):
    entidades_del_tipo_definido = obtener_entidades_del_tipo_de_modelo(modelo_tipo, modelo_dependiente)
    for entidad in entidades_del_tipo_definido:
        connection.set_tenant(entidad)
        kwargs = {
            "tipo": modelo_dependiente[0],
            campo_asociamiento: entidad
        }
        sql = ("%s %s")%("CREATE OR REPLACE VIEW reportes_tenantcafview AS", SQL_SELECCION_VISTA_TENANT_CAF)
        entidades_de_las_cuales_depende = modelo_dependiente[1].objects.filter(**kwargs)
        for no_dependiente in entidades_de_las_cuales_depende:
            sql = ("%s UNION %s")%\
            (
                sql,
                ("SELECT * FROM %s.reportes_tenantcafview E")%(no_dependiente.schema_name)
            )
        ejecutar_sql(sql)