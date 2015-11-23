#encoding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
import ast
from django.db.models import F, Count
from reportes.formularios.escenarios import FiltrosEscenariosDMDForm
from entidades.modelos_vistas_reportes import PublicEscenarioView
from reportes.models import TenantEscenarioView
from snd.modelos.deportistas import *


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
def ejecutar_consulta_segun_filtro(categoria, cantidad, departamentos,municipios, disciplinas,tipoTenant, tabla):
    """
    Noviembre 19, 2015
    Autor: Karent Narvaez

    Permite ejecutar una consulta con base en los filtros que se están enviando en la petición.
    """
    #Departamentos, municipios y disciplinas
    if departamentos and municipios and disciplinas:
        escenarios = list(tabla.objects.filter(estado=0, ciudad__departamento__id__in=departamentos, ciudad__id__in=municipios,tipodisciplinadeportiva__id__in=disciplinas).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True)))
    #Departamentos, municipios
    elif departamentos and municipios:
        escenarios = list(tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos,ciudad__id__in=municipios).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True)))
    #Departamentos, disciplinas
    elif departamentos and disciplinas:
        escenarios =  list(tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos,tipodisciplinadeportiva__id__in=disciplinas).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(categoria, distinct=True)))
    #Municipios y disciplinas
    elif municipios and disciplinas:
        escenarios = list(tabla.objects.filter(estado=0,ciudad__id__in=municipios,tipodisciplinadeportiva__id__in=disciplinas).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True)))
    #Departamentos
    elif departamentos:
        escenarios = list(tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True)))

    #Municipios
    elif municipios:
        escenarios = list(tabla.objects.filter(estado=0,ciudad__id__in=municipios).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True)))
    #Disciplina
    elif disciplinas:
        escenarios = list(tabla.objects.filter(estado=0,tipodisciplinadeportiva__id__in=disciplinas).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True)))
    #Sin filtros
    else:
        escenarios =  list(tabla.objects.filter(estado=0).annotate(descripcion=F(categoria)).values('id','descripcion').annotate(cantidad=Count(cantidad, distinct=True)))

    escenarios = tipoTenant.ajustar_resultado(escenarios)#qué hace esto?

    return escenarios


def generador_reporte_escenario(request, categoria, cantidad):

    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicEscenarioView
    else:
        tabla = TenantEscenarioView

    departamentos = None
    municipios = None
    disciplinas = None

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        try:
            municipios = None if request.GET['municipios'] == 'null'  else ast.literal_eval(request.GET['municipios'])
        except Exception:
            municipios = None
        disciplinas = None if request.GET['disciplinas'] == 'null'  else ast.literal_eval(request.GET['disciplinas'])

    escenarios = ejecutar_consulta_segun_filtro(categoria, cantidad, departamentos, municipios, disciplinas, tipoTenant, tabla)

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

    categoria = 'estrato'
    cantidad = 'estrato'

    escenarios = generador_reporte_escenario(request,categoria,cantidad)
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


def tipos_escenarios(request):
    """
    Noviembre 19, 2015
    Autor: Karent Narvaez

    Permite conocer el numero de escenarios por cada tipo de escenarios.
    """
    
    categoria = 'tipo_escenario__descripcion'
    cantidad = 'tipo_escenario'

    escenarios = generador_reporte_escenario(request, categoria, cantidad)

    if request.is_ajax():
        
        return JsonResponse(escenarios)
        
    visualizaciones = [1, 5 , 6]
    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones)
    return render(request, 'escenarios/base_escenario.html', {
        'nombre_reporte' : 'Tipos de Escenarios',
        'url_data' : 'reportes_escenarios_tipos',
        'datos': escenarios,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Escenarios'
    })


def estado_fisico(request):
    """
    Noviembre 20, 2015
    Autor: Karent Narvaez

    Permite conocer el numero de escenarios por cada condición de estado físico.
    """

    categoria = 'estado_fisico'
    cantidad = 'estado_fisico'

    escenarios = generador_reporte_escenario(request, categoria, cantidad)

    if request.is_ajax():
        
        return JsonResponse(escenarios)

    visualizaciones = [1, 5 , 6]
    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones)
    return render(request, 'escenarios/base_escenario.html', {
        'nombre_reporte' : 'Estados Físicos de Escenarios',
        'url_data' : 'reportes_escenarios_estado_fisico',
        'datos': escenarios,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Escenarios'
    })

def tipo_superficie(request):
    """
    Noviembre 20, 2015
    Autor: Karent Narvaez

    Permite conocer el numero de escenarios por cada tipo de superficie.
    """

    categoria = 'tiposuperficie__descripcion'
    cantidad = 'tiposuperficie'

    escenarios = generador_reporte_escenario(request, categoria, cantidad)

    if request.is_ajax():
        
        return JsonResponse(escenarios)

    visualizaciones = [1, 5 , 6]
    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones)
    return render(request, 'escenarios/base_escenario.html', {
        'nombre_reporte' : 'Tipo de Superficie de Escenarios',
        'url_data' : 'reportes_escenarios_tipo_superficie',
        'datos': escenarios,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Escenarios'
    })

def propietarios_escenarios(request):
    """
    Noviembre 22, 2015
    Autor: Cristian Leonardo Ríos López

    Permite conocer el numero de escenarios por su tipo de propietario(Oficial o privado).
    """

    categoria = 'tipo_propietario'
    cantidad = 'tipo_propietario'

    escenarios = generador_reporte_escenario(request, categoria, cantidad)

    if request.is_ajax():
        return JsonResponse(escenarios)

    visualizaciones = [1, 5 , 6]
    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones)
    return render(request, 'escenarios/base_escenario.html', {
        'nombre_reporte' : 'Tipo de Propietarios de Escenarios',
        'url_data' : 'reportes_escenarios_tipo_propietario',
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

    categoria = 'periodicidad'
    cantidad = 'periodicidad'

    escenarios = generador_reporte_escenario(request, categoria, cantidad)

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

def division_territorial(request):
    """
    Noviembre 20, 2015
    Autor: Andres Serna

    Permite conocer el numero de escenarios por division territorial.
    """

    categoria = 'ciudad__departamento__nombre'
    cantidad = 'ciudad__departamento'

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        if departamentos:
            categoria = 'ciudad__nombre'
            cantidad = 'ciudad'

    escenarios = generador_reporte_escenario(request, categoria, cantidad)

    if request.is_ajax():
        return JsonResponse(escenarios)

    visualizaciones = [1, 5 , 6]

    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones, eliminar='municipios')
    return render(request, 'escenarios/base_escenario.html', {
        'nombre_reporte' : 'División Territorial de Escenarios',
        'url_data' : 'reportes_escenarios_division_territorial',
        'datos': escenarios,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Escenarios'
    })