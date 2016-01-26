from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from snd.models import *
from entidades.modelos_de_datos_tenantnacional import MODELOS_DE_DATOS
from operator import attrgetter, methodcaller
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from entidades.models import Entidad


def obtenerCantidadColumnas(request, modelo):
    columnas = MODELOS_DE_DATOS[modelo][2]
    cantidadDeColumnas = len(columnas)
    if cantidadDeColumnas == 0:
        modeloBD = MODELOS_DE_DATOS[modelo][0]
        cantidadDeColumnas = len(modeloBD._meta.get_all_field_names())

    return {'cantidadDeColumnas': cantidadDeColumnas, 'columnas': columnas, 'url': reverse('cargar_datos_tenantnacional', args=[modelo])}

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
                    connection.set_tenant(modelo.entidad)
                    ContentType.objects.clear_cache()
                    try:
                        valor = render_to_string("configuracionDataTables.html", {"tipo": "ManyToMany", "valores": valor.all()})
                    except Exception as e:
                        print(e)
                    connection.set_schema_to_public()
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


def generarFilas(objetos, atributos, configuracionDespliegue, urlsOpciones):
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
            urls.append(datosURL)

        acciones = render_to_string("configuracionDataTables.html", {"tipo": "urlsOpciones", "urls": urls})
        aux.append(acciones)
        
        
        datos.append(aux)
    return datos

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
        objetos = realizarFiltroDeCampos(modeloTipo, atributos, busqueda)
        cantidadObjetos = len(objetos)
        datos['recordsTotal'] = cantidadObjetos
        datos['recordsFiltered'] = cantidadObjetos
    else:

        objetos = []
        entidades = Entidad.objects.exclude(schema_name='public')
        for entidad in entidades:
            connection.set_tenant(entidad)
            ContentType.objects.clear_cache()
            qs = modeloTipo.objects.filter(estado__in=[0,2])
            for objeto in qs:
                objetos.append(objeto)
        connection.set_schema_to_public()
        cantidadObjetos = len(objetos)
        datos['recordsTotal'] = cantidadObjetos
        datos['recordsFiltered'] = cantidadObjetos
    objetos = definirCantidadDeObjetos(objetos, inicio, fin, columna, direccion)
    datos['data'] = generarFilas(objetos, atributos, configuracionDespliegue, urlsOpciones)

    return {'datos':datos, 'nombreDeColumnas': nombreDeColumnas+["Opciones"]}

def realizarFiltroDeCampos(modeloTipo, atributos, busqueda):
    qs = modeloTipo.objects.none()
    objetos = []
    busqueda = busqueda.split(" ")

    entidades = Entidad.objects.exclude(schema_name='public')
    for entidad in entidades:
        connection.set_tenant(entidad)
        ContentType.objects.clear_cache()
        for atributo in atributos:
            arregloAtributos = atributo.split(" ")
            for elementoAtributo in arregloAtributos:
                for palabra in busqueda:
                    instruccion = "%s__contains" % elementoAtributo
                    query = {instruccion : palabra}

                    try:
                        qs = qs | modeloTipo.objects.filter(**query).filter(estado=0)
                    except Exception:
                        pass
        for objeto in qs:
            objetos.append(objeto)
    connection.set_schema_to_public()

    return objetos

def definirCantidadDeObjetos(objetos, inicio, fin, columna, direccion):
    columna = columna.split(" ")[0]
    orden = False
    if direccion == 'desc':
        orden = True

    llave = None
    if len(objetos) > 0:
        if getattr(objetos[0],columna).__class__ == str:
            llave = attrgetter(columna)
        else:
            llave = methodcaller('__str__')

    objetos_procesados = sorted(objetos, key=llave, reverse=orden)
    return objetos_procesados[inicio:fin]