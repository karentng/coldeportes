#encoding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
import ast
from django.db.models import F, Count
from entidades.modelos_vistas_reportes import PublicEscenarioView
from reportes.formularios.escenarios import FiltrosEscenariosDMDForm
from reportes.models import TenantEscenarioView, TenantEscenarioEstratoView
from snd.modelos.escenarios import *


'''
Reportes:
    1. Dona
    2. Comparativa Horizontal
    3. Comparativa Vertical
    4. Tree Map
    5. Gráfica de cilindros
    6. Gráfica de cono
    7. Gráfica de radar
'''
def verificar_seleccion_reporte(opcion_reporte):
    categoria = 'clase_acceso'
    if opcion_reporte == 'ES':
        categoria = 'estrato'
    elif opcion_reporte == 'CA':
        categoria = 'clase_acceso'
    elif opcion_reporte == 'DT':
        categoria = 'ciudad__departamento__nombre'
    elif opcion_reporte == 'EF':
        categoria = 'estado_fisico'
    elif opcion_reporte == 'TE':
        categoria = 'tipo_escenario__descripcion'
    elif opcion_reporte == 'TS':
        categoria = 'tiposuperficie__descripcion'
    elif opcion_reporte == 'TP':
        categoria = 'tipo_propietario'

    return categoria


def ejecutar_consulta_segun_filtro(categoria, cantidad, departamentos,municipios, disciplinas,tipoTenant, tabla, choices):
    """
    Noviembre 19, 2015
    Autor: Karent Narvaez

    Permite ejecutar una consulta con base en los filtros que se están enviando en la petición.
    """
    from reportes.utilities import sumar_datos_diccionario#, convert_choices_to_array, crear_diccionario_inicial

    #Departamentos, municipios y disciplinas
    if departamentos and municipios and disciplinas:
        escenarios = tabla.objects.filter(estado=0, ciudad__departamento__id__in=departamentos, ciudad__in=municipios,tipodisciplinadeportiva__in=disciplinas).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True))
    #Departamentos, municipios
    elif departamentos and municipios:
        escenarios = tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos,ciudad__in=municipios).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True))
    #Departamentos, disciplinas
    elif departamentos and disciplinas:
        escenarios = tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos,tipodisciplinadeportiva__in=disciplinas).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True))
    #Municipios y disciplinas
    elif municipios and disciplinas:
        escenarios = tabla.objects.filter(estado=0,ciudad__in=municipios,tipodisciplinadeportiva__in=disciplinas).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True))
    #Departamentos
    elif departamentos:
        escenarios = tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True))

    #Municipios
    elif municipios:
        escenarios = tabla.objects.filter(estado=0,ciudad__in=municipios).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True))
    #Disciplina
    elif disciplinas:
        escenarios = tabla.objects.filter(estado=0,tipodisciplinadeportiva__in=disciplinas).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True))
    #Sin filtros
    else:
        escenarios =  tabla.objects.filter(estado=0).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True))

    if choices:
        escenarios = sumar_datos_diccionario(escenarios,choices)
        return escenarios

    escenarios = tipoTenant.ajustar_resultado(escenarios)
    return escenarios


def generador_reporte_escenario(request, tabla, cantidad,choices=None):

    tipoTenant = request.tenant.obtenerTenant()

    departamentos = None
    municipios = None
    disciplinas = None
    reporte = None

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        municipios = None if request.GET['municipios'] == 'null'  else ast.literal_eval(request.GET['municipios'])
        disciplinas = None if request.GET['disciplinas'] == 'null'  else ast.literal_eval(request.GET['disciplinas'])
        reporte = None if request.GET['reporte'] == 'null'  else ast.literal_eval(request.GET['reporte'])

    categoria = verificar_seleccion_reporte(reporte)
    escenarios = ejecutar_consulta_segun_filtro(categoria, cantidad, departamentos, municipios, disciplinas, tipoTenant, tabla, choices)

    if '' in escenarios:
        escenarios['Ninguna'] = escenarios['']
        del escenarios['']
    return escenarios



def estrato_escenarios(request):
    """
    Noviembre 20, 2015
    Autor: Cristian Leonardo Ríos López

    Permite conocer el numero de escenarios por el estrato del escenario.
    """

    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicEscenarioEstratoView
    else:
        tabla = TenantEscenarioEstratoView

    
    cantidad = 'estrato'

    escenarios = generador_reporte_escenario(request,tabla,categoria,cantidad, choices=Escenario.estratos)
    if request.is_ajax():
        return JsonResponse(escenarios)

    visualizaciones = [1, 5 , 6]
    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones)
    return render(request, 'escenarios/base_escenario.html', {
        'nombre_reporte' : 'Estrato de Escenarios',
        'url_data' : 'reportes_escenarios_estrato',
        'datos': escenarios,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Escenarios'
    })


def caracteristicas_escenarios(request):
    """
    Noviembre 19, 2015
    Autor: Karent Narvaez

    Permite conocer el numero de escenarios por cada tipo de escenarios.
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicEscenarioView
    else:
        tabla = TenantEscenarioView
    
    cantidad = 'tipo_escenario'

    escenarios = generador_reporte_escenario(request, tabla, cantidad, choices=None)

    if request.is_ajax():
        
        return JsonResponse(escenarios)
        
    visualizaciones = [1, 5 , 6]
    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones)
    return render(request, 'escenarios/base_escenario.html', {
        'nombre_reporte' : 'Tipos de Escenarios',
        'url_data' : 'reportes_caracteristicas_escenarios',
        'datos': escenarios,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Escenarios'
    })

def periodicidad_mantenimiento(request):
    """
    Noviembre 22, 2015
    Autor: Cristian Leonardo Ríos López

    Permite conocer el numero de escenarios por su periodicidad de mantenimiento
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicEscenarioView
    else:
        tabla = TenantEscenarioView

    categoria = 'periodicidad'
    cantidad = 'periodicidad'

    escenarios = generador_reporte_escenario(request, tabla, categoria, cantidad)

    if request.is_ajax():
        return JsonResponse(escenarios)

    visualizaciones = [1, 5 , 6]

    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones)
    return render(request, 'escenarios/base_escenario.html', {
        'nombre_reporte' : 'Periodicidad de mantenimiento de Escenarios',
        'url_data' : 'reportes_escenarios_periodicidad_mantenimiento',
        'datos': escenarios,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Escenarios'
    })



def disponibilidad_escenarios(request):
    """
    Noviembre 21, 2015
    Autor: Milton Lenis

    Permite conocer los días de disponibilidad de los escenarios
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicEscenarioView
    else:
        tabla = TenantEscenarioView

    categoria = 'dias__nombre'
    cantidad = 'dias'

    escenarios = generador_reporte_escenario(request, tabla, categoria, cantidad)

    visualizaciones = [1,2,3,5,6,7]
    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones)
    return render(request, 'escenarios/base_escenario.html', {
        'nombre_reporte' : 'Días de disponibilidad de los escenarios',
        'url_data' : 'reportes_disponibilidad_escenarios',
        'datos': escenarios,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Escenarios'
    })