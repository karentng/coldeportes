from entidades.models import *

CONSULTA, TENANT, PUBLIC = [None, None, None]

    
def alter_campo_escenarios():
    from django.db import connection
    from reportes.crear_vistas_actores.sql_generadores import COMANDOS_GENERADORES_DE_VISTAS_ACTORES

    def ejecutar_sql(sql):
        cursor = connection.cursor()
        r=''
        r=cursor.execute(sql)
        r=connection.commit()
        return r

    todos_los_tenants = Entidad.objects.exclude(schema_name='public').order_by('id')

    for tenant in todos_los_tenants:
        sql = ("ALTER TABLE %s.snd_caracterizacionescenario ALTER COLUMN capacidad_espectadores TYPE integer USING (capacidad_espectadores::integer);")%(tenant.schema_name)
        try:
            ejecutar_sql(sql)
        except Exception:
            pass

def generar_vistas(nuevo_tenant=None, padre=None):
    from django.db import connection
    from reportes.crear_vistas_actores.sql_generadores import COMANDOS_GENERADORES_DE_VISTAS_ACTORES

    def ejecutar_sql(sql):
        cursor = connection.cursor()
        r=''
        r=cursor.execute(sql)
        r=connection.commit()
        return r

    def eliminar_vista_materializada_public():
        sql = ("DROP MATERIALIZED VIEW IF EXISTS %s;")%(PUBLIC)
        ejecutar_sql(sql)

    def generar_vista_materializada_public():
        todos_los_tenants = Entidad.objects.exclude(schema_name='public').order_by('id')
        primero = todos_los_tenants[0]
        todos_los_tenants = todos_los_tenants[1:]

        sql = ("%s %s")%\
        (
            ("CREATE MATERIALIZED VIEW %s AS")%(PUBLIC),
            CONSULTA(primero.schema_name)
            #("SELECT * FROM %s.%s E")%(primero.schema_name, TENANT)
        )

        for tenant in todos_los_tenants:
            #sql_tenant = ("SELECT * FROM %s.%s E")%(tenant.schema_name, TENANT)
            sql_tenant = CONSULTA(tenant.schema_name)
            sql = ("%s UNION %s")%(sql, sql_tenant)

        eliminar_vista_materializada_public()
        ejecutar_sql(sql)

    def generar_vista_caf_nuevo_tenant(nuevo_tenant):
        connection.set_tenant(nuevo_tenant)
        ejecutar_sql(("CREATE OR REPLACE VIEW %s AS %s")%(TENANT, CONSULTA()))

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
        print(padre)
        if padre:
            print ("PADRE")
            print(padre)
            parametros = obtener_parametros_generacion_vista(padre)
            print (parametros)
            connection.set_tenant(padre)
            kwargs = {
                "tipo": parametros[0][0],
                parametros[1]: padre
            }
            sql = ("CREATE OR REPLACE VIEW %s AS %s")%(TENANT, CONSULTA())
            entidades_de_las_cuales_depende = parametros[0][1].objects.filter(**kwargs)
            for no_dependiente in entidades_de_las_cuales_depende:
                sql = ("%s UNION %s")%\
                (
                    sql,
                    ("SELECT * FROM %s.%s E")%(no_dependiente.schema_name, TENANT)
                )
            print(sql)
            ejecutar_sql(sql)

    def generar_vista_caf_independientes():
        entidades = Entidad.objects.filter(tipo__in=[3, 4, 5, 9, 10, 11])
        for entidad in entidades:
            connection.set_tenant(entidad)
            ejecutar_sql(("CREATE OR REPLACE VIEW %s AS %s")%(TENANT, CONSULTA()))

    def generar_vista_caf_dependientes(modelo_tipo, modelo_dependiente, campo_asociamiento):
        def obtener_entidades_del_tipo_de_modelo(modelo_tipo, modelo_dependiente):
            if modelo_tipo == Comite:
                if modelo_dependiente[1] == Federacion:
                    return modelo_tipo.objects.filter(schema_name="coc")
                return modelo_tipo.objects.filter(schema_name="cpc")
            else:
                return modelo_tipo.objects.exclude(schema_name="public")

        entidades_del_tipo_definido = obtener_entidades_del_tipo_de_modelo(modelo_tipo, modelo_dependiente)
        for entidad in entidades_del_tipo_definido:
            connection.set_tenant(entidad)
            kwargs = {
                "tipo": modelo_dependiente[0],
                campo_asociamiento: entidad
            }
            sql = ("CREATE OR REPLACE VIEW %s AS %s")%(TENANT, CONSULTA())
            entidades_de_las_cuales_depende = modelo_dependiente[1].objects.filter(**kwargs)
            for no_dependiente in entidades_de_las_cuales_depende:
                sql = ("%s UNION %s")%\
                (
                    sql,
                    ("SELECT * FROM %s.%s E")%(no_dependiente.schema_name, TENANT)
                )
            ejecutar_sql(sql)

    def eliminar_vistas_actuales(tenant, public):
        entidades = Entidad.objects.exclude(schema_name="public")
        drop = "DROP VIEW"
        for i in entidades:
            sql = ("%s %s.%s CASCADE")%(drop, i.schema_name, tenant)
            try:
                ejecutar_sql(sql)
            except Exception as e:
                print(e)
        #sql = ("DROP MATERIALIZED VIEW %s")%(public)
        #ejecutar_sql(sql)

    def inicio_generacion(nuevo_tenant, padre):
        def acomodar_comandos(comandos):
            global CONSULTA
            global TENANT
            global PUBLIC
            CONSULTA, TENANT, PUBLIC = comandos

        for i in COMANDOS_GENERADORES_DE_VISTAS_ACTORES:
            acomodar_comandos(i)
            if nuevo_tenant: # Solo se actualiza el padre del creado si existe
                generar_vista_caf_nuevo_tenant(nuevo_tenant)
                generar_vista_caf_padre_nuevo_tenant(nuevo_tenant.obtener_padre())
                generar_vista_caf_padre_nuevo_tenant(padre)
            else: # se deben actualizar todos
                eliminar_vistas_actuales(TENANT, PUBLIC)
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

    inicio_generacion(nuevo_tenant, padre)