# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from datetime import date
from django.contrib.auth.models import *
from snd.models import Deportista, PersonalApoyo, Escenario

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
            if valor == True:
                permitidos.append(i[0])
        except Exception as e:
            print (e)
            pass
    return permitidos

def tenant_actor(actor):
    """
    Agosto 05 / 2015
    Autor: Andrés Serna

    Función que verifica si el tenant tiene tiene acceso al actor especificado
    :param actor:  Actor que se verificará
    :type actor:   String
    :returns:      Redirección al inicio (No tenía permisos) o a la página deseada (Si tenía permisos)
    :rtype:        HttpResponseRedirect
    """
    def decorator(a_view):
        def _wrapped_view(request, *args, **kwargs):
            try:
                valor = hasattr(request.tenant.actores, actor)
                if valor == True:
                    valor = getattr(request.tenant.actores, actor)
                    if valor == True:
                        return a_view(request, *args, **kwargs)
                    else:
                        print ("No tiene los permisos para el actor: %s"%(actor))
                        return redirect('inicio')
                else:
                    print ("Actor %s no existente"%(actor))
                    return redirect('inicio')
            except Exception as e:
                return a_view(request, *args, **kwargs)
            return a_view(request, *args, **kwargs)
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

def not_transferido_required(objeto):
    """
    Agosto 17 / 2015
    Autor: Daniel Correa

    Permite validar si el estado del objeto es diferente a En transferencia o Transferido para ejecutar una funcionalidad de una vista

    :param objeto: objeto transferible
    """
    if objeto.estado in (2,3):
        return redirect('inicio_tenant')

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