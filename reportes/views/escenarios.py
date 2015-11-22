#encoding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
import ast
from django.db.models import F, Count
from reportes.formularios.escenarios import EstratoForm, FiltrosEscenariosDMDForm
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
        escenarios = list(tabla.objects.filter(estado=0, ciudad__departamento__id__in=departamentos, ciudad__id__in=municipios,tipodisciplinadeportiva__id__in=disciplinas).annotate(descripcion=F(categoria)).values('descripcion').annotate(cantidad=Count(cantidad, distinct=True)))
    #Departamentos, municipios
    elif departamentos and municipios:
        escenarios = list(tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos,ciudad__id__in=municipios).annotate(descripcion=F(categoria)).values('descripcion').annotate(cantidad=Count(cantidad, distinct=True)))    
    #Departamentos, disciplinas
    elif departamentos and disciplinas:
        escenarios =  list(tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos,tipodisciplinadeportiva__id__in=disciplinas).annotate(descripcion=F(categoria)).values('descripcion').annotate(cantidad=Count(categoria, distinct=True))),
    #Municipios y disciplinas
    elif municipios and disciplinas:
        escenarios = list(tabla.objects.filter(estado=0,ciudad__id__in=municipios,tipodisciplinadeportiva__id__in=disciplinas).annotate(descripcion=F(categoria)).values('descripcion').annotate(cantidad=Count(cantidad, distinct=True)))
    #Departamentos
    elif departamentos:
        escenarios = list(tabla.objects.filter(estado=0,ciudad__departamento__id__in=departamentos).annotate(descripcion=F(categoria)).values('descripcion').annotate(cantidad=Count(cantidad, distinct=True)))
    #Municipios
    elif municipios:
        escenarios = list(tabla.objects.filter(estado=0,ciudad__id__in=municipios).annotate(descripcion=F(categoria)).values('descripcion').annotate(cantidad=Count(cantidad, distinct=True)))
    #Disciplina
    elif disciplinas:
        print('entro m')
        escenarios = list(tabla.objects.filter(estado=0,tipodisciplinadeportiva__id__in=disciplinas).annotate(descripcion=F(categoria)).values('descripcion').annotate(cantidad=Count(cantidad, distinct=True)))
    #Sin filtros
    else:
        escenarios =  list(tabla.objects.filter(estado=0).annotate(descripcion=F(categoria)).values('descripcion').annotate(cantidad=Count(cantidad, distinct=True)))

    escenarios = tipoTenant.ajustar_resultado(escenarios)

    return escenarios

def generador_reporte_escenario(request, categoria, cantidad):

    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicEscenarioView
    else:
        tabla = TenantEscenarioView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        municipios = None if request.GET['municipios'] == 'null'  else ast.literal_eval(request.GET['municipios'])
        disciplinas = None if request.GET['disciplinas'] == 'null'  else ast.literal_eval(request.GET['disciplinas'])

        escenarios = ejecutar_consulta_segun_filtro(categoria, cantidad, departamentos, municipios, disciplinas, tipoTenant, tabla)

        if '' in escenarios:
            escenarios['Ninguna'] = escenarios['']
            del escenarios['']

        return JsonResponse(escenarios)

    else:
        escenarios = ejecutar_consulta_segun_filtro(categoria, cantidad, None, None, None, tipoTenant, tabla)

        if '' in escenarios:
            escenarios['NO APLICA'] = escenarios['']
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
        tabla = PublicEscenarioView
    else:
        tabla = TenantEscenarioView

    consultas = [
            "list(%s.objects.filter(estado=0))"
        ]

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        municipios = None if request.GET['municipios'] == 'null'  else ast.literal_eval(request.GET['municipios'])
        disciplinas = None if request.GET['disciplinas'] == 'null'  else ast.literal_eval(request.GET['disciplinas'])

        escenarios = ejecutar_consulta_segun_filtro(consultas,departamentos,municipios,disciplinas,tipoTenant,tabla)

        return JsonResponse(escenarios)

    else:
        #Traer la cantidad de hisotriales ordenados por tipo
        escenarios = tipoTenant.ejecutar_consulta(True, consultas[len(consultas)-1])

    visualizaciones = [1, 2, 3, 5]
    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones)
    return render(request, 'base_reportes.html', {
        'nombre_reporte' : 'Estratos de Escenarios',
        'url_data' : 'reportes_escenarios_estrato',
        'datos': escenarios,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas'
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

    visualizaciones = [1, 5 , 6]
    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones)
    return render(request, 'escenarios/tipo_escenario.html', {
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

    visualizaciones = [1, 5 , 6]
    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones)
    return render(request, 'escenarios/tipo_escenario.html', {
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

    visualizaciones = [1, 5 , 6]
    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones)
    return render(request, 'escenarios/tipo_escenario.html', {
        'nombre_reporte' : 'Tipo de Superficie de Escenarios',
        'url_data' : 'reportes_escenarios_tipo_superficie',
        'datos': escenarios,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Escenarios'
    })