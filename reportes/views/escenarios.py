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

def estrato(request):
    tipoTenant = request.tenant.obtenerTenant()

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        annos = None if request.GET['annos'] == 'null'  else ast.literal_eval(request.GET['annos'])
        disciplina = None if request.GET['disciplina'] == 'null' else ast.literal_eval(request.GET['disciplina'])
        
        return JsonResponse({})
    else:
        escenarios = tipoTenant.ejecutar_consulta(False, "list(Escenario.objects.annotate(descripcion_=F('estrato')).values('descripcion_').annotate(cantidad=Count('estrato')))")
    visualizaciones = [1, 2, 3]

    form = EstratoForm(visualizaciones=visualizaciones)
    return render(request, 'escenarios/estrato.html', {
        'escenarios': escenarios,
        'visualizaciones': visualizaciones,
        'form': form,
    })


def tipos_escenarios(request):
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

    categoria = 'tipo_escenario__descripcion'
    cantidad = 'tipo_escenario'

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        municipios = None if request.GET['municipios'] == 'null'  else ast.literal_eval(request.GET['municipios'])
        disciplinas = None if request.GET['disciplinas'] == 'null'  else ast.literal_eval(request.GET['disciplinas'])

        tipos = ejecutar_consulta_segun_filtro(categoria, cantidad, departamentos, municipios, disciplinas, tipoTenant, tabla)

        if '' in tipos:
            tipos['Ninguna'] = tipos['']
            del tipos['']

        return JsonResponse(tipos)

    else:
        tipos = ejecutar_consulta_segun_filtro(categoria, cantidad, None, None, None, tipoTenant, tabla)

        if '' in tipos:
            tipos['NO APLICA'] = tipos['']
            del tipos['']

    visualizaciones = [1, 5 , 6]
    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones)
    return render(request, 'escenarios/tipo_escenario.html', {
        'nombre_reporte' : 'Tipos de Escenarios',
        'url_data' : 'reportes_escenarios_tipos',
        'datos': tipos,
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
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicEscenarioView
    else:
        tabla = TenantEscenarioView

    categoria = 'estado_fisico'
    cantidad = 'estado_fisico'

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