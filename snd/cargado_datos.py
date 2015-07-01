from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from snd.models import *
from django.http import HttpResponse
from django.db.models import Q
from snd.modelos_de_datos import MODELOS_DE_DATOS
import operator
import json

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
        else:
            valor = ('%s'%getattr(modelo, campo))
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
        objetos = modelo.objects.all()
        cantidadObjetos = len(objetos)
        datos['recordsTotal'] = cantidadObjetos
        datos['recordsFiltered'] = cantidadObjetos

    objetos = definirCantidadDeObjetos(objetos, inicio, fin, columna, direccion)

    datos['data'] = generarFilas(objetos, atributos, configuracionDespliegue, urlsOpciones)
    
    return {'datos':datos, 'nombreDeColumnas': nombreDeColumnas+["Opciones"]}

def realizarFiltroDeCampos(modeloTipo, atributos, busqueda):
    objetos = modeloTipo.objects.none()
    busqueda = busqueda.split(" ")

    Qr = None
    for atributo in atributos:
        arregloAtributos = atributo.split(" ")
        for elementoAtributo in arregloAtributos:
            for palabra in busqueda:
                instruccion = "%s__contains" % elementoAtributo
                query = {instruccion : palabra}

                try:
                    objetos = objetos | modeloTipo.objects.filter(**query)
                except Exception:
                    pass

    return objetos

def definirCantidadDeObjetos(objetos, inicio, fin, columna, direccion):
    orden = ''
    if direccion == 'desc':
        orden = "-"

    return objetos.order_by(orden+columna)[inicio:fin]