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

def ejecutar_consulta_segun_filtro(categoria, cantidad, departamentos, municipios, tipoTenant, tabla, choices):
    """
    Noviembre 19, 2015
    Autor: Karent Narvaez

    Permite ejecutar una consulta con base en los filtros que se están enviando en la petición.
    """
    from reportes.utilities import sumar_datos_diccionario#, convert_choices_to_array, crear_diccionario_inicial

    if departamentos and municipios:
        dirigentes = tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos,ciudad__in=municipios).annotate(descripcion=F(categoria)).exclude(descripcion=None).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))
    #Departamentos, disciplinas
    elif departamentos:
        dirigentes = tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos).annotate(descripcion=F(categoria)).exclude(descripcion=None).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))
    #Municipios
    elif municipios:
        dirigentes = tabla.objects.filter(estado=0,ciudad__in=municipios).annotate(descripcion=F(categoria)).exclude(descripcion=None).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))
    #Disciplina
    else:
        dirigentes =  tabla.objects.filter(estado=0).annotate(descripcion=F(categoria)).exclude(descripcion=None).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))

    if choices:
        dirigentes = sumar_datos_diccionario(dirigentes, choices)
        return dirigentes

    dirigentes = tipoTenant.ajustar_resultado(dirigentes)
    return dirigentes

def generador_reporte_dirigentes(request, tabla, cantidad, categoria, choices=None):

    tipoTenant = request.tenant.obtenerTenant()

    departamentos = None
    municipios = None

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        municipios = None if request.GET['municipios'] == 'null'  else ast.literal_eval(request.GET['municipios'])
    
    dirigentes = ejecutar_consulta_segun_filtro(categoria, cantidad, departamentos, municipios, tipoTenant, tabla, choices)

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
    
    cantidad = 'nacionalidad'
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
    })