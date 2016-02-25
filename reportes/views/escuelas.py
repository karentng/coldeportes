#encoding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import F, Count

import ast
from datetime import date, datetime

from entidades.modelos_vistas_reportes import PublicEscuelaView
from reportes.formularios.escuelas import EscuelasForm
from reportes.models import TenantEscuelaView
from snd.models import EscuelaDeportiva

def ejecutar_consulta_segun_filtro(categoria, cantidad, departamentos, municipios, tipoTenant, tabla, choices):
    """
    Noviembre 19, 2015
    Autor: Karent Narvaez

    Permite ejecutar una consulta con base en los filtros que se están enviando en la petición.
    """
    from reportes.utilities import sumar_datos_diccionario#, convert_choices_to_array, crear_diccionario_inicial

    if departamentos and municipios:
        escuelas = tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos,ciudad__in=municipios).annotate(descripcion=F(categoria)).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))
    #Departamentos, disciplinas
    elif departamentos:
        escuelas = tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos).annotate(descripcion=F(categoria)).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))
    #Municipios
    elif municipios:
        escuelas = tabla.objects.filter(estado=0,ciudad__in=municipios).annotate(descripcion=F(categoria)).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))
    #Disciplina
    else:
        try:
            escuelas =  tabla.objects.filter(estado=0).annotate(descripcion=F(categoria)).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))
        except Exception as e:
            print(e)

    if choices:
        escuelas = sumar_datos_diccionario(escuelas, choices)
        return escuelas

    escuelas = tipoTenant.ajustar_resultado(escuelas)
    return escuelas

def generador_reporte_escuelas(request, tabla, cantidad, categoria, choices=None):

    tipoTenant = request.tenant.obtenerTenant()

    departamentos = None
    municipios = None

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        municipios = None if request.GET['municipios'] == 'null'  else ast.literal_eval(request.GET['municipios'])
    
    escuelas = ejecutar_consulta_segun_filtro(categoria, cantidad, departamentos, municipios, tipoTenant, tabla, choices)

    if None in escuelas:
        escuelas['Ninguna'] = escuelas[None]
        del escuelas[None]

    return escuelas

def estrato_escuelas(request):
    """
    Enero 2, 2016
    Autor: Cristian Leonardo Ríos López

    Permite conocer el número de escuelas de formaicón deportiva por su estrato.
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicEscuelaView
    else:
        tabla = TenantEscuelaView
    
    cantidad = 'id'
    categoria = 'estrato'
    escuelas = generador_reporte_escuelas(request, tabla, cantidad, categoria, choices=EscuelaDeportiva.ESTRATOS)
    
    if request.is_ajax():
        return JsonResponse(escuelas)
        
    visualizaciones = [1, 5, 6]
    form = EscuelasForm(visualizaciones=visualizaciones)
    return render(request, 'escuelas/base_escuelas.html', {
        'nombre_reporte' : 'Escuelas de formación deportiva por estrato',
        'url_data' : 'reportes_estrato_escuelas',
        'datos': escuelas,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Escuelas de Formación Deportiva',
        'fecha_generado': datetime.now(),
        'nombre_columna':'Estrato'
    })

def servicios_escuelas(request):
    """
    Enero 2, 2016
    Autor: Cristian Leonardo Ríos López

    Permite conocer el número de escuelas de formación deportiva según los servicios que presta.
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicEscuelaView
    else:
        tabla = TenantEscuelaView
    
    cantidad = 'id'
    categoria = 'nombre_servicio'
    escuelas = generador_reporte_escuelas(request, tabla, cantidad, categoria, choices=None)
    
    if request.is_ajax():
        return JsonResponse(escuelas)
        
    visualizaciones = [1, 5, 6]
    form = EscuelasForm(visualizaciones=visualizaciones)
    return render(request, 'escuelas/base_escuelas.html', {
        'nombre_reporte' : 'Escuelas de formación deportiva por servicios prestados',
        'url_data' : 'reportes_servicios_escuelas',
        'datos': escuelas,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Escuelas de Formación Deportiva',
        'fecha_generado': datetime.now(),
        'nombre_columna':'Servicio'
    })