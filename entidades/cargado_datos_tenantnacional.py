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
    try:
        condicion_es_actor_propio = type(condiciones[0][0] is list) and condiciones[0][0][0] == 'entidad'
    except Exception:
        condicion_es_actor_propio = False

    if condiciones == None:
        return True
    # Aplica el operador AND (Editado por Milton)
    cumple = True
    if type(condiciones[0][0]) is str:
        for permiso in condiciones[0]:
            cumple = cumple and request.user.has_perm(permiso)
        #En el caso de que se cumplan todos los permisos anteriores, debemos verificar las condiciones siguientes
        #que pueden o no existir
        if cumple:
            #Verificamos si hay más condiciones por verificar
            try:
                condiciones[1]
                hay_mas_condiciones = True
            except Exception as e:
                hay_mas_condiciones = False
            #Si hay más condiciones verificamos cada una de ellas.
            if hay_mas_condiciones:
                condiciones_array = condiciones[1:len(condiciones)]
                for i in condiciones_array:
                    valoresDeAtributos = evaluarAtributos(objeto, i[0])
                    atributosDefinidos = i[1]
                    ok = i[2](valoresDeAtributos, atributosDefinidos)

                    if ok == True:
                        return ok
            else:
                return cumple
        else:
            return False
    elif condicion_es_actor_propio:
        try:
            if objeto.entidad == request.tenant:
                return True
        except Exception: # No tiene entidad
            return False
    else:
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
        objetos = modeloTipo.objects.filter(estado__in=[0,2]).order_by('id','entidad').distinct('id','entidad')
        cantidadObjetos = len(objetos)
        datos['recordsTotal'] = cantidadObjetos
        datos['recordsFiltered'] = cantidadObjetos
    objetos = definirCantidadDeObjetos(objetos, inicio, fin, columna, direccion)
    datos['data'] = generarFilas(objetos, atributos, configuracionDespliegue, urlsOpciones)

    return {'datos':datos, 'nombreDeColumnas': nombreDeColumnas+["Opciones"]}

def realizarFiltroDeCampos(modeloTipo, atributos, busqueda):
    objetos = modeloTipo.objects.none()
    busqueda = busqueda.split(" ")

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
                            objeto = modeloTipo.objects.filter(**query).filter(estado__in=[0,2]).order_by('id','entidad').distinct('id','entidad')
                            objetos = objetos | objeto
                else:
                    try:
                        instruccion = "%s__nombre__icontains" % elementoAtributo
                        query = {instruccion : palabra}
                        objeto = modeloTipo.objects.filter(**query).filter(estado__in=[0,2]).order_by('id','entidad').distinct('id','entidad')
                    except Exception:
                        instruccion = "%s__icontains" % elementoAtributo
                        query = {instruccion : palabra}
                        objeto = modeloTipo.objects.filter(**query).filter(estado__in=[0,2]).order_by('id','entidad').distinct('id','entidad')
                    finally:
                        objetos = objetos | objeto
    return objetos

def definirCantidadDeObjetos(objetos, inicio, fin, columna, direccion):
    from operator import methodcaller
    import operator
    columna = columna.split(" ")[0]
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