#encoding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
import ast
from reportes.formularios.escenarios import EstratoForm

'''
Reportes:
    1. Dona
    2. Comparativa Horizontal
    3. Comparativa Vertical
    4. Tree Map
'''
def ejecutar_consulta_segun_filtro(consultas,departamentos,municipios, disciplinas,tipoTenant):
    """
    Noviembre 19, 2015
    Autor: Karent Narvaez

    Permite ejecutar una consulta con base en los filtros que se están enviando en la petición.
    """
    if departamentos and municipios and disciplinas:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[0]%(departamentos,municipios,disciplinas))

    elif departamentos and municipios:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[1]%(departamentos,municipios))

    elif departamentos and disciplinas:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[2]%(departamentos,disciplinas))

    elif municipios and disciplinas:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[3]%(municipios,disciplinas))

    elif departamentos:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[4]%(departamentos))

    elif municipios:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[5]%(municipios))

    elif disciplinas:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[6]%(disciplinas))

    else:
        escenarios = tipoTenant.ejecutar_consulta(True,consultas[7])

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


def etinias_deportistas(request):
    """
    Noviembre 13, 2015
    Autor: Daniel Correa

    Permite conocer el numero de deportistas ordenados por etnias
    """
    tipoTenant = request.tenant.obtenerTenant()
    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        consultas = [
            "list(Deportista.objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('etnia')).values('descripcion').annotate(cantidad=Count('etnia')))",
            "list(Deportista.objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('etnia')).values('descripcion').annotate(cantidad=Count('etnia')))",
            "list(Deportista.objects.filter(estado=0,genero__in=%s).annotate(descripcion=F('etnia')).values('descripcion').annotate(cantidad=Count('etnia')))",
            "list(Deportista.objects.filter(estado=0).annotate(descripcion=F('etnia')).values('descripcion').annotate(cantidad=Count('etnia')))",
        ]

        etnias = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)

        if '' in etnias:
            etnias['Ninguna'] = etnias['']
            del etnias['']

        return JsonResponse(etnias)

    else:
        etnias = tipoTenant.ejecutar_consulta(True, "list(Deportista.objects.filter(estado=0).annotate(descripcion=F('etnia')).values('descripcion').annotate(cantidad=Count('etnia')))")

        if '' in etnias:
            etnias['NO APLICA'] = etnias['']
            del etnias['']

    visualizaciones = [1, 2, 3]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'base_reportes.html', {
        'nombre_reporte' : 'Etnias de los deportistas',
        'url_data' : 'reporte_etinias_deportistas',
        'datos': etnias,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas'
    })