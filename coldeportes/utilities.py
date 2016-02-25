# -*- encoding: utf-8 -*-
from functools import wraps
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect,render
from datetime import date
from django.contrib.auth.models import *
from datetimewidget.widgets import DateWidget, DateTimeWidget
import urllib.parse

def get_request_or_none(request, field):
    import ast
    try:
        return None if request[field] == 'null'  else ast.literal_eval(request[field])
    except Exception as e:
        return None

def MyDateWidget():
    return DateWidget(usel10n=False, bootstrap_version=3, options={'format': 'yyyy-mm-dd', 'startView':4, 'language':'es'})

def MyDateTimeWidget():
    return DateTimeWidget(usel10n=False, bootstrap_version=3, options={'format': 'yyyy-mm-dd HH:ii', 'startView':4, 'language':'es'})

def permisos_de_tipo(entidad,perms):
    """
    Noviembre 4,2015
    Autor: Daniel Correa

    Funcion que permite validar los permisos de una entidad segun su tipo

    :param entidad: entidad a evaluar
    :param perms: arreglo de tipos
    :return: valor de aceptacion, paso o no la prueba
    """
    if entidad.tipo in perms:
        return True
    return False

def verificar_tamano_archivo(self, datos, campo):
    from django.forms import ValidationError
    from django.core.files.uploadedfile import InMemoryUploadedFile

    MAX_UPLOAD_SIZE_MB = 5
    MAX_UPLOAD_SIZE = 1048576 * MAX_UPLOAD_SIZE_MB # 5MB: http://www.beesky.com/newsite/bit_byte.htm

    archivo = datos[campo]

    tipo = type(archivo)
    if not tipo is bool:
        if tipo is InMemoryUploadedFile:
            try:
                if archivo._size > MAX_UPLOAD_SIZE:
                    from django.forms.util import ErrorList
                    if not campo in self._errors:
                        self._errors[campo] = ErrorList()
                    self._errors[campo].append("El tamaño del archivo no debe ser mayor a %s MB"%(MAX_UPLOAD_SIZE_MB))
            except Exception:
                pass
        else:
            print ("No esta en memoria")
    else:
        print ("Es bool")
    return self

def extraer_codigo_video(url_video):

    url_data = urllib.parse.urlparse(url_video)
    query = urllib.parse.parse_qs(url_data.query)
    video = query["v"][0]

    return video

def inicializarComponentes():
    """
    Agosto 05 / 2015
    Autor: Andrés Serna

    Función para cambiar la representacion en String de la clase Permission
    """
    def representacionStringPermisos(self):
        return self.name
    Permission.__str__ = representacionStringPermisos
inicializarComponentes()

def tenant_required(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.tenant.tipo in [2,6,7]:
            raise PermissionDenied
        else:
            return function(request, *args, **kwargs)

    return decorator

def all_permission_required(*perms):
    """
    Agosto 05 / 2015
    Autor: Andrés Serna

    Función que revisa si todos los permisos ingresados se cumplen
    :param perms: Lista con los permisos a revisar
    :type perms:  Lista de String's
    :returns:     Verdadero si cumple, Falso en caso contrario
    :rtype:       Boolean
    """
    return user_passes_test(lambda u: all(u.has_perm(perm) for perm in perms))

def any_permission_required(*perms):
    """
    Agosto 05 / 2015
    Autor: Andrés Serna

    Función que revisa si alguno de los permisos ingresados se cumple
    :param perms: Lista con los permisos a revisar
    :type perms:  Lista de String's
    :returns:     Verdadero si cumple, Falso en caso contrario
    :rtype:       Boolean
    """
    return user_passes_test(lambda u: any(u.has_perm(perm) for perm in perms))

def permisosPermitidos(request, permisos):
    """
    Agosto 05 / 2015
    Autor: Andrés Serna

    Función que retorna los permisos permitidos por el tenant
    :param request:  Petición realizada
    :type request:   WSGIRequest
    :param permisos: Matriz de permisos con el campo que indica si es permitido o no
    :type permisos:  Lista de lista de String's
    :returns:        Permisos permitidos por el tenant
    :rtype:          Lista de String's
    """
    permitidos = []
    for i in permisos:
        try:
            valor = getattr(request.tenant.actores, i[1])
            if valor:
                permitidos.append(i[0])
        except Exception as e:
            print (e, "Excepción en función permisosPermitidos, coldeportes.utilities")
            pass
    return permitidos


def tenant_actor(actor):
    """
    Noviembre 14 / 2015
    Autor: Cristian Leonardo Ríos López

    Función que verifica si el tenant tiene tiene acceso al actor especificado
    :param actor:  Actor que se verificará
    :type actor:   String
    :returns:      Redirección a la página 403 (No tenía permisos) o a la página deseada (Si tenía permisos)
    :rtype:        HttpResponseRedirect
    """
    def decorator(a_view):
        def _wrapped_view(request, *args, **kwargs):
            try:
                permisos = Group.objects.get(name="Solo lectura").permissions.all()
                permisos_text = []
                for permiso in permisos:
                    permisos_text.append(permiso.codename)
                if 'view_'+actor in permisos_text:
                    return a_view(request, *args, **kwargs)
                else:
                    return render(request,'403.html',{})
            except Group.DoesNotExist:
                return render(request,'403.html',{})
        return _wrapped_view
    return decorator

def superuser_only(function):
    """
    Agosto 05 / 2015
    Autor: Andrés Serna

    Función que verifica si el usuario logueado es un super usuario
    :param function:  Función a ejecutar si es super usuario
    :type function:   Function
    :returns:         Redirección al inicio sino es super usuario o a la página deseada si lo es
    :rtype:           HttpResponseRedirect
    """
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('login')
        return function(request, *args, **kwargs)
    return _inner

def adicionarClase(campo, clase):
    """
    Agosto 05 / 2015
    Autor: Andrés Serna

    Función para agregar clases a un campo de formulario
    :param campo: Campo del formulario
    :type campo:  Field
    :param clase: Clase que se le adicionará al campo
    :type clase:  String
    :returns:     Campo del formulario con la clase agregada
    :rtype:       Field
    """
    campo.widget.attrs.update({'class': clase})
    if clase == 'fecha':
        campo.widget.attrs.update({'readonly': True})
        campo.widget.format = '%Y-%m-%d'
        campo.input_formats=('%Y-%m-%d',)
    campo.widget.attrs.update({'class': clase})
    return campo

def calculate_age(born):
    """
    Junio 22 / 2015
    Autor: Daniel Correa

    Funcion para el calculo de la edad de acuerdo a una fecha ingresada por parametro
    :param born: Fecha de nacimiento de la persona a calcular edad
    :type born: Datetime.date
    """

    today = date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError: # caso de  February 29 en año no bisiesto
        birthday = born.replace(year=today.year, month=born.month+1, day=1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year

def not_transferido_required(request,objeto):
    """
    Agosto 17 / 2015
    Autor: Daniel Correa

    Permite validar si el estado del objeto es diferente a En transferencia o Transferido para ejecutar una funcionalidad de una vista

    :param objeto: objeto transferible
    """
    if objeto.estado in (2,3):
        return render(request,'403.html',{})

'''
    Julio 15 / 2015
    Funciones que verifican los decoradores definidos y si cumple agrega el patrón de url a grupo de patrones
'''
def required(wrapping_functions,patterns_rslt):
    if not hasattr(wrapping_functions,'__iter__'): 
        wrapping_functions = (wrapping_functions,)

    return [
        _wrap_instance__resolve(wrapping_functions,instance)
        for instance in patterns_rslt
    ]

def _wrap_instance__resolve(wrapping_functions,instance):
    if not hasattr(instance,'resolve'): return instance
    resolve = getattr(instance,'resolve')

    def _wrap_func_in_returned_resolver_match(*args,**kwargs):
        rslt = resolve(*args,**kwargs)
        if not hasattr(rslt,'func'):return rslt
        f = getattr(rslt,'func')
        for _f in reversed(wrapping_functions):
            f = _f(f)
        setattr(rslt,'func',f)
        return rslt
    
    setattr(instance,'resolve',_wrap_func_in_returned_resolver_match)
    return instance

'''
    Octubre 26/2015
    Autor: Cristian Leonardo Ríos López
    Descripción: Permite agregar los actores obligatorios a una entidad
'''
def add_actores(model,actores):

    #estos son los actores que se tienen por obligación
    '''ACTORES = {
        '1': ['selecciones'],#Liga
        '2': ['selecciones'],#Federacion
        '3': [],#Club
        '4': ['cajas'],#CajaDeCompensacion
        '5': ['normas'],#Ente
        '6': ['selecciones'],#Comite
        '7': ['selecciones'],#FederacionParalimpica
        '8': ['selecciones'],#LigaParalimpica
        '9': ['deportistas'],#clubParalimpico
        '10': ['centros'],#Caf
        '11': ['deportistas','escuelas_deportivas']#EscuelaDeportiva_
    }
    #Todos tienen
    actores.personal_apoyo = True
    actores.dirigentes = True
    actores.noticias = True

    actores_agregar = ACTORES[tipo]
    for actor in actores_agregar:
        setattr(actores, actor, True)'''

    for actor in actores:
        setattr(model,actor,True)

def refresh_public():
    from django.db import connection
    sql_tenant = """
        REFRESH MATERIALIZED VIEW entidades_publiccafview;
        REFRESH MATERIALIZED VIEW entidades_publicescenarioview;
        REFRESH MATERIALIZED VIEW entidades_publicpersonalapoyoview;
        REFRESH MATERIALIZED VIEW entidades_publicdeportistaview;
        REFRESH MATERIALIZED VIEW entidades_publicdirigenteview;
        REFRESH MATERIALIZED VIEW entidades_publicescuelaview;
    """
    try:
        cursor = connection.cursor()
        r=''
        r=cursor.execute(sql_tenant)
        r=connection.commit()
    except Exception as e:
        print (("%s %s")%("Error en refresh_public (coldeportes.utilities.py): ", e))



"""
    Autor: Milton Lenis
    Fecha: Febrero 9 de 2016

    Función que toma el nombre de un actor y retorna el modelo del snd que lo representa.
"""

def obtener_modelo_actor(actor):
    from snd.modelos.cafs import CentroAcondicionamiento
    from snd.modelos.escenarios import Escenario
    from snd.modelos.deportistas import Deportista
    from snd.modelos.personal_apoyo import PersonalApoyo
    from snd.modelos.cajas_compensacion import CajaCompensacion
    from snd.modelos.selecciones import Seleccion
    from snd.modelos.centro_biomedico import CentroBiomedico
    from snd.modelos.escuela_deportiva import EscuelaDeportiva
    from normograma.models import Norma
    from noticias.models import Noticia

    if actor =='centros':
        return CentroAcondicionamiento
    elif actor=='escenarios':
        return Escenario
    elif actor=='deportistas':
        return Deportista
    elif actor=='personal_apoyo':
        return PersonalApoyo
    elif actor=='dirigentes':
        return Dirigente
    elif actor=='cajas':
        return CajaCompensacion
    elif actor=='selecciones':
        return Seleccion
    elif actor=='centros_biomedicos':
        return CentroBiomedico
    elif actor=='normas':
        return Norma
    elif actor=='escuelas_deportivas':
        return EscuelaDeportiva
    elif actor=='noticias':
        return Noticia
    else:
        return None
