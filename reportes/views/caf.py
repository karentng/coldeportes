#encoding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import F, Count

import ast
from datetime import date, datetime

from entidades.modelos_vistas_reportes import PublicCafView
from reportes.formularios.caf import DemografiaForm, FiltrosCafDMDForm
from reportes.models import TenantCafView
from snd.models import CentroAcondicionamiento

'''
Reportes:
    1. Dona
    2. Comparativa Horizontal
    3. Comparativa Vertical
    4. Tree Map
    5. Gráfico de cilindros
'''

def ejecutar_consulta_segun_filtro(categoria, cantidad, departamentos, municipios, tipoTenant, tabla, choices):
    """
    Noviembre 19, 2015
    Autor: Karent Narvaez

    Permite ejecutar una consulta con base en los filtros que se están enviando en la petición.
    """
    from reportes.utilities import sumar_datos_diccionario#, convert_choices_to_array, crear_diccionario_inicial

    if departamentos and municipios:
        cafs = tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos,ciudad__in=municipios).annotate(descripcion=F(categoria)).exclude(descripcion=None).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))
    #Departamentos, disciplinas
    elif departamentos:
        cafs = tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos).annotate(descripcion=F(categoria)).exclude(descripcion=None).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))
    #Municipios
    elif municipios:
        cafs = tabla.objects.filter(estado=0,ciudad__in=municipios).annotate(descripcion=F(categoria)).exclude(descripcion=None).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))
    #Disciplina
    else:
        cafs =  tabla.objects.filter(estado=0).annotate(descripcion=F(categoria)).exclude(descripcion=None).values('id','descripcion', 'entidad_id').annotate(cantidad=Count(cantidad, distinct=True))

    if choices:
        cafs = sumar_datos_diccionario(cafs, choices)
        return cafs

    cafs = tipoTenant.ajustar_resultado(cafs)
    return cafs


def obtener_choices_categoria(categoria):
    if categoria == 'estrato':
        return CentroAcondicionamiento.ESTRATOS
    else:
        return None


def verificar_seleccion_reporte(opcion_reporte):
    categoria = 'ciudad__departamento__nombre'
    if opcion_reporte == 'DT':
        categoria = 'ciudad__departamento__nombre'
    elif opcion_reporte == 'ES':
        categoria = 'estrato'
    elif opcion_reporte == 'CC':
        categoria = 'nombre_clase'
    elif opcion_reporte == 'SC':
        categoria = 'nombre_servicio'
    return categoria


def generador_reporte_caf(request, tabla, cantidad,choices=None):

    tipoTenant = request.tenant.obtenerTenant()

    departamentos = None
    municipios = None
    reporte = None

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        municipios = None if request.GET['municipios'] == 'null'  else ast.literal_eval(request.GET['municipios'])
        reporte = None if request.GET['reporte'] == 'null'  else ast.literal_eval(request.GET['reporte'])
    
    categoria = verificar_seleccion_reporte(reporte)

    choices = obtener_choices_categoria(categoria)
    print(choices)

    cafs = ejecutar_consulta_segun_filtro(categoria, cantidad, departamentos, municipios, tipoTenant, tabla, choices)

    if '' in cafs:
        cafs['Ninguna'] = cafs['']
        del cafs['']

    return cafs

def caracteristicas_caf(request):
    """
    Diciembre 12, 2015
    Autor: Andrés Serna

    Permite conocer el numero de caf por cada tipo de caf.
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicCafView
    else:
        tabla = TenantCafView
    
    cantidad = 'id'
    cafs = generador_reporte_caf(request, tabla, cantidad, choices=None)
    
    if request.is_ajax():
        return JsonResponse(cafs)
        
    visualizaciones = [1, 2, 3, 5, 6, 7]
    form = FiltrosCafDMDForm(visualizaciones=visualizaciones)
    nombres_columnas = ["Departamento", "Estrato", "Clase", "Servicio"]
    return render(request, 'caf/base_caf.html', {
        'nombre_reporte' : 'Centros de acondicionamiento por departamento',
        'url_data' : 'reportes_caracteristicas_caf',
        'datos': cafs,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Centro de Acondicionamiento Físico',
        'fecha_generado': datetime.now(),
        'nombres_columnas': nombres_columnas,
    })