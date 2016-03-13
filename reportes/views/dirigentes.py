#encoding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import F, Count

import ast
from datetime import date, datetime

from entidades.modelos_vistas_reportes import PublicDirigenteView
from reportes.formularios.dirigentes import NacionalidadForm
from reportes.models import TenantDirigenteView
from snd.models import Dirigente


def ejecutar_consulta_segun_filtro(categoria, cantidad, departamentos, genero, tipoTenant, tabla, choices):
    """
    Noviembre 19, 2015
    Autor: Karent Narvaez

    Permite ejecutar una consulta con base en los filtros que se están enviando en la petición.
    """
    from reportes.utilities import sumar_datos_diccionario
    if departamentos and genero:
        dirigentes = tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos,genero__in=genero).annotate(descripcion=F(categoria)).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))
    #Departamentos
    elif departamentos:
        dirigentes = tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos).annotate(descripcion=F(categoria)).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))
    #Genero
    elif genero:
        dirigentes = tabla.objects.filter(estado=0,genero__in=genero).annotate(descripcion=F(categoria)).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))
    #Disciplina
    else:
        dirigentes =  tabla.objects.filter(estado=0).annotate(descripcion=F(categoria)).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))

    if choices:
        dirigentes = sumar_datos_diccionario(dirigentes, choices)
        return dirigentes

    dirigentes = tipoTenant.ajustar_resultado(dirigentes)
    return dirigentes

def generador_reporte_dirigentes(request, tabla, cantidad, categoria, choices=None):

    tipoTenant = request.tenant.obtenerTenant()

    departamentos = None
    #municipios = None
    genero = None
    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        #municipios = None if request.GET['municipios'] == 'null'  else ast.literal_eval(request.GET['municipios'])

    dirigentes = ejecutar_consulta_segun_filtro(categoria, cantidad, departamentos, genero, tipoTenant, tabla, choices)

    if '' in dirigentes:
        dirigentes['Ninguna'] = dirigentes['']
        del dirigentes['']

    return dirigentes

def nacionalidad_dirigentes(request):
    """
    Diciembre 31, 2015
    Autor: Cristian Leonardo Ríos López

    Permite conocer el numero de dirigentes segun su nacionalidad.
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicDirigenteView
    else:
        tabla = TenantDirigenteView
    
    cantidad = 'id'
    categoria = 'nacionalidad__nombre'
    dirigentes = generador_reporte_dirigentes(request, tabla, cantidad, categoria, choices=None)
    
    if request.is_ajax():
        return JsonResponse(dirigentes)
        
    visualizaciones = [1, 5, 6]
    form = NacionalidadForm(visualizaciones=visualizaciones)
    return render(request, 'dirigentes/base_dirigentes.html', {
        'nombre_reporte' : 'Nacionalidad de los dirigentes',
        'url_data' : 'reportes_nacionalidad_dirigentes',
        'datos': dirigentes,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Dirigentes',
        'fecha_generado': datetime.now(),
        'nombre_columna': 'Nacionalidades'
    })

def ejecutar_filtros(consultas,departamentos,genero,tipoTenant):
    """
    Noviembre 13, 2015
    Autor: Daniel Correa

    Permite ejecutar los diferentes filtros de casos de acuerdo a un arreglo de consultas
    CONSULTAS LLEVA EL SIGUIENTE FORMATO [contulta caso 1, consulta caso 2 , consulta caso 3, ... ,consulta caso n]
    LOS CASOS EMPIEZAN EN 1 EL DE MAS ARRIBA HASTA N EL DE MAS ABAJO
    """
    if departamentos and genero:
        resultado = eval(consultas[0]%(departamentos,genero))
    elif departamentos:
        resultado = eval(consultas[1]%(departamentos))
    elif genero:
        resultado = eval(consultas[2]%(genero))
    else:
        resultado = eval(consultas[3])
    return resultado

def cantidad_dirigentes(request):
    """
    Marzo 8 de 2016
    Autor: Yalile Bermudes Saavedra

    Permite conocer la cantidad de dirigentes por municipio o departamento.
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicDirigenteView
    else:
        tabla = TenantDirigenteView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null' else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])


        consultas = [
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad__departamento__id__in=%s,genero__in=%s).values('id','entidad').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad__departamento__id__in=%s).values('id','entidad').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,genero__in=%s).values('id','entidad').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0).values('id','entidad').annotate(cantidad=Count('id',distinct=True)))",
        ]

        total_dirigentes = len(ejecutar_filtros(consultas,departamentos,genero, tipoTenant))

        resultado = {
            'Total Dirigentes':total_dirigentes
        }

        return JsonResponse(resultado)

    else:
        total_dirigentes = len(tabla.objects.filter(estado = 0).values('id','entidad').annotate(cantidad=Count('id',distinct=True)))

        resultado = {
            'Total Dirigentes':total_dirigentes
        }

    visualizaciones = [1]
    form = NacionalidadForm(visualizaciones=visualizaciones)
    return render(request, 'dirigentes/base_dirigentes.html', {
        'nombre_reporte' : 'Cantidad total de dirigentes',
        'url_data' : 'reportes_cantidad_dirigentes',
        'datos': resultado,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Dirigentes',
        'fecha_generado': datetime.now(),
        'nombres_columnas':"Descripción"
    })