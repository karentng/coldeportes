#encoding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
import ast
from django.db.models import F, Count
from reportes.formularios.escenarios import EstratoForm, FiltrosEscenariosDMDForm
from entidades.modelos_vistas_reportes import PublicEscenarioView
from reportes.models import TenantEscenarioView


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
def ejecutar_consulta_segun_filtro(consultas,departamentos,municipios, disciplinas,tipoTenant, tabla):
    """
    Noviembre 19, 2015
    Autor: Karent Narvaez

    Permite ejecutar una consulta con base en los filtros que se están enviando en la petición.
    """
    if departamentos and municipios and disciplinas:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[0]%(tabla,departamentos,municipios,disciplinas))

    elif departamentos and municipios:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[1]%(tabla,departamentos,municipios))

    elif departamentos and disciplinas:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[2]%(tabla,departamentos,disciplinas))

    elif municipios and disciplinas:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[3]%(tabla,municipios,disciplinas))

    elif departamentos:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[4]%(tabla,departamentos))

    elif municipios:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[5]%(tabla,municipios))

    elif disciplinas:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[6]%(tabla,disciplinas))

    else:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[7]%(tabla))

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
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicEscenarioView
    else:
        tabla = TenantEscenarioView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        municipios = None if request.GET['municipios'] == 'null'  else ast.literal_eval(request.GET['municipios'])
        disciplinas = None if request.GET['disciplinas'] == 'null'  else ast.literal_eval(request.GET['disciplinas'])

        consultas = [
            "list(%s.objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,ciudad_residencia__id__in=%s,tipo_disciplinas__id__in=%s).annotate(descripcion=F('tipo_escenario__descripcion')).values('descripcion').annotate(cantidad=Count('tipo_escenario')))",
            "list(%s.objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,ciudad_residencia__id__in=%s,tipo_disciplinas__id__in=%s).annotate(descripcion=F('tipo_escenario__descripcion')).values('descripcion').annotate(cantidad=Count('tipo_escenario__descripcion')))",
            "list(%s.objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,ciudad_residencia__id__in=%s,tipo_disciplinas__id__in=%s).annotate(descripcion=F('tipo_escenario__descripcion')).values('descripcion').annotate(cantidad=Count('tipo_escenario__descripcion')))",
            "list(%s.objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,ciudad_residencia__id__in=%s,tipo_disciplinas__id__in=%s).annotate(descripcion=F('tipo_escenario__descripcion')).values('descripcion').annotate(cantidad=Count('tipo_escenario__descripcion')))",
            "list(%s.objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,ciudad_residencia__id__in=%s,tipo_disciplinas__id__in=%s).annotate(descripcion=F('tipo_escenario__descripcion')).values('descripcion').annotate(cantidad=Count('tipo_escenario__descripcion')))",
            "list(%s.objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,ciudad_residencia__id__in=%s,tipo_disciplinas__id__in=%s).annotate(descripcion=F('tipo_escenario__descripcion')).values('descripcion').annotate(cantidad=Count('tipo_escenario__descripcion')))",
            "list(%s.objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,ciudad_residencia__id__in=%s,tipo_disciplinas__id__in=%s).annotate(descripcion=F('tipo_escenario__descripcion')).values('descripcion').annotate(cantidad=Count('tipo_escenario__descripcion')))",
            "list(%s.objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,ciudad_residencia__id__in=%s,tipo_disciplinas__id__in=%s).annotate(descripcion=F('tipo_escenario__descripcion')).values('descripcion').annotate(cantidad=Count('tipo_escenario')))",
            
        ]

        tipos = ejecutar_consulta_segun_filtro(consultas,departamentos,genero,tipoTenant, tabla)

        if '' in tipos:
            tipos['Ninguna'] = tipos['']
            del tipos['']

        return JsonResponse(tipos)

    else:
        tipos = list(tabla.objects.filter(estado=0).annotate(descripcion=F('tipo_escenario__descripcion')).values('descripcion').annotate(cantidad=Count('tipo_escenario')))

        if '' in tipos:
            tipos['NO APLICA'] = tipos['']
            del tipos['']

    visualizaciones = [1, 5 , 6]
    form = FiltrosEscenariosDMDForm(visualizaciones=visualizaciones)
    return render(request, 'base_reportes.html', {
        'nombre_reporte' : 'Tipos de Escenarios',
        'url_data' : 'reportes_escenarios_tipos',
        'datos': tipos,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Escenarios'
    })