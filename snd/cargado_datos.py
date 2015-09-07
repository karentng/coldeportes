from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from snd.models import *
from django.http import HttpResponse
from django.db.models import Q
from snd.modelos_de_datos import MODELOS_DE_DATOS
import operator
import json
from operator import methodcaller
from coldeportes.settings import STATIC_URL,MEDIA_URL
from entidades.models import Club
from entidades.models import Liga, LigaParalimpica


def obtenerCantidadColumnas(request, modelo):
    columnas = MODELOS_DE_DATOS[modelo][2]
    cantidadDeColumnas = len(columnas)
    if cantidadDeColumnas == 0:
        modeloBD = MODELOS_DE_DATOS[modelo][0]
        cantidadDeColumnas = len(modeloBD._meta.get_all_field_names())

    return {'cantidadDeColumnas': cantidadDeColumnas, 'columnas': columnas, 'url': reverse('cargar_datos', args=[modelo])}

def obtenerAtributosModelo(modelo):
    atributos = MODELOS_DE_DATOS[modelo][1]
    nombreDeColumnas = MODELOS_DE_DATOS[modelo][2]
    configuracionDespliegue = MODELOS_DE_DATOS[modelo][3]
    urlsOpciones = MODELOS_DE_DATOS[modelo][4]
    modelo = MODELOS_DE_DATOS[modelo][0]

    if atributos == None:
        nombreDeColumnas = []
        atributos = modelo._meta.get_all_field_names()
        for i in atributos:
            nombreDeColumnas.append(i.upper())
    
    return [modelo, atributos, nombreDeColumnas, configuracionDespliegue, urlsOpciones]

def obtenerOrganizacionDatos(request, atributos):
    inicio = int(request.GET['start'])
    fin = inicio + int(request.GET['length'])
    columna = atributos[int(request.GET['order[0][column]'])]
    direccion = request.GET['order[0][dir]']

    return [inicio, fin, columna, direccion]

def obtenerDato(modelo, campos):
    valor = None

    campos = campos.split(" ")

    if len(campos) == 1:
        campo = campos[0]
        if hasattr(modelo, 'get_%s_display' % campo):
            valor = (getattr(modelo, 'get_%s_display' % campo)())
        elif '.' in campo:
            atributos = campo.split('.')
            valor = modelo
            for atributo in atributos:
                valor = getattr(valor,atributo)
        else:
            try:
                valor = getattr(modelo, campo)
                if valor.__class__.__name__ == 'ManyRelatedManager':
                    valor = render_to_string("configuracionDataTables.html", {"tipo": "ManyToMany", "valores": valor.all()})
                elif valor.__class__.__name__ == 'method':
                    valor = valor()
                    valor = ('%s'%valor)
                if valor.__class__.__name__ == "ImageFieldFile":
                    valor = render_to_string("configuracionDataTables.html", {"tipo": "foto", "valor": valor,"MEDIA_URL":MEDIA_URL,"STATIC_URL":STATIC_URL})
                else:
                    valor = ('%s'%valor)
            except Exception:
                return campo

    else:
        valor = ''
        for campo in campos:
            if hasattr(modelo, 'get_%s_display' % campo):
                valor = ("%s %s")%(valor, (getattr(modelo, 'get_%s_display' % campo)()))
            else:
                valor = ("%s %s")%(valor, ('%s'%getattr(modelo, campo)))

    return valor

def evaluarAtributos(objeto, atributos):
    valores = []
    for i in atributos:
        valores.append(obtenerDato(objeto, i))
    return valores

def evaluarCondiciones(objeto, condiciones):
    if condiciones == None:
        return True
    # Aplica el operador OR
    for i in condiciones:
        valoresDeAtributos = evaluarAtributos(objeto, i[0])
        atributosDefinidos = i[1]
        ok = i[2](valoresDeAtributos, atributosDefinidos)
        if ok == True:
            return ok
    return False


def generarFilas(objetos, atributos, configuracionDespliegue, urlsOpciones,request):
    datos = []
    for objeto in objetos:
        aux = []

        if configuracionDespliegue != None:
            for conf in configuracionDespliegue:
                columnaConfiguracion = conf[0]
                configuraciones = conf[1]

                for atributo in atributos:
                    valor = obtenerDato(objeto, atributo)
                    if columnaConfiguracion == atributo:
                        for configuracion in configuraciones:
                            if valor == configuracion[0]:
                                valor = render_to_string("configuracionDataTables.html",
                                    {
                                        "tipo": configuracion[1],
                                        "label": valor
                                    }
                                )
                                aux.append(valor)
                    else:
                        aux.append(valor)
        else:
            for atributo in atributos:
                valor = obtenerDato(objeto, atributo)
                aux.append(valor)

        urls = []

        for i in urlsOpciones:
            bien = evaluarCondiciones(objeto, i[4])
            if not(bien):
                continue

            parametros = evaluarAtributos(objeto, i[2])

            datosURL = {
                "nombre": i[0],
                "url": reverse(i[1], args=parametros),
                "imagen": i[3],
            }

            #if request.tenant.tipo == 1 or request.tenant.tipo == 2 or request.tenant.tipo == 6:
            if request.tenant.tipo not in [3,5,4,8]:
                #Si no es Club, Ente, Caja o Liga Paralimpica, se trabaja en el siguiente esquema
                if objeto.__class__.__name__ == 'Dirigente' or objeto.__class__.__name__ == 'PersonalApoyo':
                    if objeto.entidad == request.tenant:
                        urls.append(datosURL)
                    else:
                        if 'ver' in datosURL['url']:
                            urls.append(datosURL)
                else:
                    urls.append(datosURL)
            else:
                urls.append(datosURL)

        acciones = render_to_string("configuracionDataTables.html", {"tipo": "urlsOpciones", "urls": urls,"objeto":objeto})
        aux.append(acciones)

        datos.append(aux)

    return datos

def obtener_objetos_por_tenant(request,modelo):
    #Tenant de tipo liga
    if request.tenant.tipo == 1:
        if modelo.__name__ == 'Seleccion':
            objetos = []
            #Saco los objetos propios de la liga
            qs = modelo.objects.all()
            for objeto in qs:
                objetos.append(objeto)
        else:
            objetos = []
            tenant_actual = request.tenant
            #Saco los objetos del modelo dado para la liga, esto se hace para el caso de dirigentes y personal_apoyo que puede tener la liga propia
            qs = modelo.objects.all()
            for objeto in qs:
                objetos.append(objeto)
            clubes = Club.objects.filter(liga=request.tenant.id)
            for club in clubes:
                connection.set_tenant(club)
                ContentType.objects.clear_cache()
                qs = modelo.objects.filter(estado=0)
                for objeto in qs:
                    objetos.append(objeto)
            connection.set_tenant(tenant_actual)
        return objetos
    #Tenant de tipo Federación
    elif request.tenant.tipo == 2:
        if modelo.__name__ == 'Seleccion':
            objetos = []
            #Saco los objetos propios de la federacion
            qs = modelo.objects.all()
            for objeto in qs:
                objetos.append(objeto)
        else:
            objetos = []
            tenant_actual = request.tenant
            #Saco los objetos propios de la federacion
            qs = modelo.objects.all()
            for objeto in qs:
                objetos.append(objeto)
            #Ligas de la federacion
            ligas = Liga.objects.filter(federacion=request.tenant.id)
            for liga in ligas:
                #saco los objetos de cada una de las ligas pertenecientes a la federación
                connection.set_tenant(liga)
                ContentType.objects.clear_cache()
                qs = modelo.objects.filter(estado=0)
                for objeto in qs:
                    objetos.append(objeto)
                #obtengo los clubes de cada liga y saco los objetos de cada uno
                clubes = Club.objects.filter(liga=liga.id)
                for club in clubes:
                    connection.set_tenant(club)
                    ContentType.objects.clear_cache()
                    qs = modelo.objects.filter(estado=0)
                    for objeto in qs:
                        objetos.append(objeto)
            connection.set_tenant(tenant_actual)
        return objetos
    #tenant de tipo Comite
    elif request.tenant.tipo == 6:
        if modelo.__name__ == 'Seleccion':
            objetos = []
            #Saco los objetos propios del comite
            qs = modelo.objects.all()
            for objeto in qs:
                objetos.append(objeto)
        else:
            objetos = []
            tenant_actual = request.tenant
            #Saco los objetos propios del comité
            qs = modelo.objects.all()
            for objeto in qs:
                objetos.append(objeto)
            #federaciones del comité
            federaciones = Federacion.objects.filter(comite=request.tenant.id)
            for federacion in federaciones:
                #saco los objetos de cada una de las federaciones pertenecientes al comité
                connection.set_tenant(federacion)
                ContentType.objects.clear_cache()
                qs = modelo.objects.filter(estado=0)
                for objeto in qs:
                    objetos.append(objeto)
                #obtengo las ligas de cada federación y saco los objetos de cada uno
                ligas = Liga.objects.filter(federacion=federacion.id)
                for liga in ligas:
                    connection.set_tenant(liga)
                    ContentType.objects.clear_cache()
                    qs = modelo.objects.filter(estado=0)
                    for objeto in qs:
                        objetos.append(objeto)
                    #obtengo los clubes de cada liga y saco los objetos de cada uno
                    clubes = Club.objects.filter(liga=liga.id)
                    for club in clubes:
                        connection.set_tenant(club)
                        ContentType.objects.clear_cache()
                        qs = modelo.objects.filter(estado=0)
                        for objeto in qs:
                            objetos.append(objeto)
            connection.set_tenant(tenant_actual)
        return objetos
    #Tenant de tipo Federación Paramilitar
    elif request.tenant.tipo == 7:
        if modelo.__name__ == 'Seleccion':
            objetos = []
            #Saco los objetos propios de la federacion paralimpica
            qs = modelo.objects.all()
            for objeto in qs:
                objetos.append(objeto)
        else:
            objetos = []
            tenant_actual = request.tenant
            #Saco los objetos propios de la federacion
            qs = modelo.objects.all()
            for objeto in qs:
                objetos.append(objeto)
            #Ligas de la federacion
            ligas = LigaParalimpica.objects.filter(federacion=request.tenant.id)
            for liga in ligas:
                #saco los objetos de cada una de las ligas pertenecientes a la federación
                connection.set_tenant(liga)
                ContentType.objects.clear_cache()
                qs = modelo.objects.filter(estado=0)
                for objeto in qs:
                    objetos.append(objeto)
            connection.set_tenant(tenant_actual)
        return objetos
    else:
        #Este es para el caso en que sea un club o el resto de entidades las cuales tienen acceso a los datos propios de su entidad solamente
        objetos = modelo.objects.all()
        return objetos


def obtenerDatos(request, modelo):

    datos = {
        "draw": int(request.GET['draw']),
        "recordsTotal": 0,
        "recordsFiltered": 0,
        "data":[]
    }

    try:
        modeloTipo, atributos, nombreDeColumnas, configuracionDespliegue, urlsOpciones = obtenerAtributosModelo(modelo)
        modelo = modeloTipo
    except Exception:
        return {'datos':datos, 'nombreDeColumnas': []}

    inicio, fin, columna, direccion = obtenerOrganizacionDatos(request, atributos)
    
    busqueda = request.GET['search[value]']
    
    if busqueda:
        objetos = realizarFiltroDeCampos(modeloTipo, atributos, busqueda,request)
        cantidadObjetos = len(objetos)
        datos['recordsTotal'] = cantidadObjetos
        datos['recordsFiltered'] = cantidadObjetos
    else:
        objetos = obtener_objetos_por_tenant(request,modelo)
        cantidadObjetos = len(objetos)
        datos['recordsTotal'] = cantidadObjetos
        datos['recordsFiltered'] = cantidadObjetos

    if request.tenant.tipo in [1,2,6,7]:
        multiples_tenant = True
    else:
        multiples_tenant = False

    objetos = definirCantidadDeObjetos(objetos, inicio, fin, columna, direccion, multiples_tenant)
    datos['data'] = generarFilas(objetos, atributos, configuracionDespliegue, urlsOpciones,request)
    
    return {'datos':datos, 'nombreDeColumnas': nombreDeColumnas+["Opciones"]}

def ejecutar_busqueda(modeloTipo,atributos,busqueda,tenant_conectar,tenant_actual):
    objetos = modeloTipo.objects.none()
    mismo_tenant = False
    if tenant_conectar.id != tenant_actual.id:
        mismo_tenant = True
        connection.set_tenant(tenant_conectar)
        ContentType.objects.clear_cache()
    for atributo in atributos:
        arregloAtributos = atributo.split(" ")
        for elementoAtributo in arregloAtributos:
            for palabra in busqueda:
                choices = modeloTipo._meta.get_field(elementoAtributo).choices
                if choices != []:
                    import re

                    for k, v in choices:
                        if re.search(palabra, v, re.IGNORECASE):
                            instruccion = "%s" % elementoAtributo
                            query = {instruccion : k}
                            objeto = modeloTipo.objects.filter(**query)
                            objetos = objetos | objeto
                else:
                    try:
                        instruccion = "%s__nombre__icontains" % elementoAtributo
                        query = {instruccion : palabra}
                        if mismo_tenant:
                            objeto = modeloTipo.objects.filter(**query)
                        else:
                            objeto = modeloTipo.objects.filter(**query).filter(estado=0)
                    except Exception:
                        instruccion = "%s__icontains" % elementoAtributo
                        query = {instruccion : palabra}
                        if mismo_tenant:
                            objeto = modeloTipo.objects.filter(**query)
                        else:
                            objeto = modeloTipo.objects.filter(**query).filter(estado=0)
                    finally:
                        objetos = objetos | objeto
    return objetos

def realizarFiltroDeCampos(modeloTipo, atributos, busqueda, request):
    busqueda = busqueda.split(" ")
    #Cuando el tipo de tenant es una liga hay que ejecutar las busquedas dentro de la liga y dentro de sus clubes
    if request.tenant.tipo == 1:
        if modeloTipo.__name__ == 'Seleccion':
            objetos = []
            tenant_actual = request.tenant
            #Saco los objetos propios de la federacion
            qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,tenant_actual,tenant_actual)
            for objeto in qs:
                objetos.append(objeto)
        else:
            objetos = []
            tenant_actual = request.tenant
            qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,tenant_actual,tenant_actual)
            for objeto in qs:
                objetos.append(objeto)
            #Buscar en cada uno de los clubes
            clubes = Club.objects.filter(liga=request.tenant.id)
            for club in clubes:
                qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,club,tenant_actual)
                for objeto in qs:
                    objetos.append(objeto)
            return objetos
    #Cuando el tipo de tenant es una federación hay que ejecutar las busquedas dentro de la federación, dentro de sus ligas y dentro de los clubes de cada liga
    elif request.tenant.tipo == 2:
        if modeloTipo.__name__ == 'Seleccion':
            objetos = []
            tenant_actual = request.tenant
            #Saco los objetos propios de la federacion
            qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,tenant_actual,tenant_actual)
            for objeto in qs:
                objetos.append(objeto)
        else:
            objetos = []
            tenant_actual = request.tenant
            qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,tenant_actual,tenant_actual)
            for objeto in qs:
                objetos.append(objeto)
            #Buscar en cada una de las ligas
            ligas = Liga.objects.filter(federacion=tenant_actual)
            for liga in ligas:
                qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,liga,tenant_actual)
                for objeto in qs:
                    objetos.append(objeto)
                #Buscar en los clubes de cada liga
                clubes = Club.objects.filter(liga=liga.id)
                for club in clubes:
                    qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,club,tenant_actual)
                    for objeto in qs:
                        objetos.append(objeto)
            return objetos
    elif request.tenant.tipo == 6:
        if modeloTipo.__name__ == 'Seleccion':
            objetos = []
            tenant_actual = request.tenant
            #Saco los objetos propios del comite
            qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,tenant_actual,tenant_actual)
            for objeto in qs:
                objetos.append(objeto)
        else:
            objetos = []
            tenant_actual = request.tenant
            qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,tenant_actual,tenant_actual)
            for objeto in qs:
                objetos.append(objeto)
            #Buscar en cada una de las federaciones
            federaciones = Federacion.objects.filter(comite=tenant_actual)
            for federacion in federaciones:
                qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,federacion,tenant_actual)
                for objeto in qs:
                    objetos.append(objeto)
                #se busca en los ligas de cada una de las federaciones
                ligas = Liga.objects.filter(federacion=federacion.id)
                for liga in ligas:
                    qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,liga,tenant_actual)
                    for objeto in qs:
                        objetos.append(objeto)
                    #Buscar en los clubes de cada liga
                    clubes = Club.objects.filter(liga=liga.id)
                    for club in clubes:
                        qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,club,tenant_actual)
                        for objeto in qs:
                            objetos.append(objeto)
            return objetos
    #Cuando el tipo de tenant es una federación paralimpica
    # hay que ejecutar las busquedas dentro de la federación, dentro de sus ligas
    elif request.tenant.tipo == 7:
        if modeloTipo.__name__ == 'Seleccion':
            objetos = []
            tenant_actual = request.tenant
            #Saco los objetos propios de la federacion paralimpica
            qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,tenant_actual,tenant_actual)
            for objeto in qs:
                objetos.append(objeto)
        else:
            objetos = []
            tenant_actual = request.tenant
            qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,tenant_actual,tenant_actual)
            for objeto in qs:
                objetos.append(objeto)
            #Buscar en cada una de las ligas
            ligas = LigaParalimpica.objects.filter(federacion=tenant_actual)
            for liga in ligas:
                qs = ejecutar_busqueda(modeloTipo,atributos,busqueda,liga,tenant_actual)
                for objeto in qs:
                    objetos.append(objeto)
            return objetos
    else:
        objetos = ejecutar_busqueda(modeloTipo,atributos,busqueda,request.tenant,request.tenant)
        return objetos


def definirCantidadDeObjetos(objetos, inicio, fin, columna, direccion,multiples_tenant):
    columna = columna.split(" ")[0]
    if multiples_tenant:
        orden = False
        if direccion == 'desc':
            orden = True

        llave = None
        if len(objetos) > 0:
            if getattr(objetos[0],columna).__class__ == str:
                llave = operator.attrgetter(columna)
            else:
                llave = methodcaller('__str__')
        objetos_procesados = sorted(objetos, key=llave, reverse=orden)
        return objetos_procesados[inicio:fin]
    else:
        orden = ''
        if direccion == 'desc':
            orden = "-"

        return objetos.order_by(orden+columna)[inicio:fin]