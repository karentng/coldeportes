#encoding:utf-8
from django.shortcuts import render, redirect
from snd.models import HistorialDeportivo,Deportista,InformacionAdicional
from entidades.models import Departamento
from django.db.models import Count
from reportes.forms import FiltrosDeportistasForm
from django.db.models import F
import ast
from django.http import JsonResponse

def ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant):
    """
    Noviembre 13, 2015
    Autor: Daniel Correa

    Permite ejecutar los diferentes filtros de casos de acuerdo a un arreglo de consultas
    CONSULTAS LLEVA EL SIGUIENTE FORMATO [contulta caso 1, consulta caso 2 , consulta caso 3, ... ,consulta caso n]
    LOS CASOS EMPIEZAN EN 1 EL DE MAS ARRIBA HASTA N EL DE MAS ABAJO
    """
    if departamentos and genero:
        participaciones = tipoTenant.ejecutar_consulta(True,consultas[0]%(departamentos,genero))
    elif departamentos:
        participaciones = tipoTenant.ejecutar_consulta(True,consultas[1]%(departamentos))
    elif genero:
        participaciones = tipoTenant.ejecutar_consulta(True,consultas[2]%(genero))
    else:
        participaciones = tipoTenant.ejecutar_consulta(True,consultas[3])

    return participaciones

def participaciones_deportivas(request):
    """
    Noviembre 13, 2015
    Autor: Daniel Correa

    Reporte participaciones deportivas:
    Consulta que trae el numero de  participaciones deportiva ordenadas por tipo
    """
    tipoTenant = request.tenant.obtenerTenant()
    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        consultas = [
            "list(HistorialDeportivo.objects.filter(deportista__estado = 0,deportista__ciudad_residencia__departamento__id__in=%s,deportista__genero__in=%s).annotate(descripcion=F('tipo')).values('descripcion').annotate(cantidad=Count('tipo')))",
            "list(HistorialDeportivo.objects.filter(deportista__estado = 0,deportista__ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('tipo')).values('descripcion').annotate(cantidad=Count('tipo')))",
            "list(HistorialDeportivo.objects.filter(deportista__estado = 0,deportista__genero__in=%s).annotate(descripcion=F('tipo')).values('descripcion').annotate(cantidad=Count('tipo')))",
            "list(HistorialDeportivo.objects.filter(deportista__estado = 0,).annotate(descripcion=F('tipo')).values('descripcion').annotate(cantidad=Count('tipo')))"


        ]

        participaciones = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)

        return JsonResponse(participaciones)

    else:
        #Traer la cantidad de hisotriales ordenados por tipo
        participaciones = tipoTenant.ejecutar_consulta(True, "list(HistorialDeportivo.objects.filter(deportista__estado = 0,).annotate(descripcion=F('tipo')).values('descripcion').annotate(cantidad=Count('tipo')))")

    visualizaciones = [1, 2, 3]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/reportes_deportistas.html', {
        'nombre_reporte' : 'Participaciones Deportivas',
        'url_data' : 'reporte_participaciones_deportivas',
        'datos': participaciones,
        'visualizaciones': visualizaciones,
        'form': form,
    })


def beneficiario_programa_apoyo(request):
    """
    Noviembre 13, 2015
    Autor: Daniel Correa

    Permite conocer el numero de deportistas beneficiados por un programa de apoyo
    """
    tipoTenant = request.tenant.obtenerTenant()
    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        consultas = [
            "list(InformacionAdicional.objects.filter(deportista__estado = 0,deportista__ciudad_residencia__departamento__id__in=%s,deportista__genero__in=%s).annotate(descripcion=F('es_beneficiario_programa_apoyo')).values('descripcion').annotate(cantidad=Count('es_beneficiario_programa_apoyo')))",
            "list(InformacionAdicional.objects.filter(deportista__estado = 0,deportista__ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('es_beneficiario_programa_apoyo')).values('descripcion').annotate(cantidad=Count('es_beneficiario_programa_apoyo')))",
            "list(InformacionAdicional.objects.filter(deportista__estado = 0,deportista__genero__in=%s).annotate(descripcion=F('es_beneficiario_programa_apoyo')).values('descripcion').annotate(cantidad=Count('es_beneficiario_programa_apoyo')))",
            "list(InformacionAdicional.objects.filter(deportista__estado = 0).annotate(descripcion=F('es_beneficiario_programa_apoyo')).values('descripcion').annotate(cantidad=Count('es_beneficiario_programa_apoyo')))"
        ]

        participaciones = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)

        return JsonResponse(participaciones)

    else:
        #Traer la cantidad de hisotriales ordenados por tipo
        participaciones = tipoTenant.ejecutar_consulta(True, "list(InformacionAdicional.objects.filter(deportista__estado = 0).annotate(descripcion=F('es_beneficiario_programa_apoyo')).values('descripcion').annotate(cantidad=Count('es_beneficiario_programa_apoyo')))")

    visualizaciones = [1, 2, 3]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/reportes_deportistas.html', {
        'nombre_reporte' : 'Participaciones Deportivas',
        'url_data' : 'reporte_participaciones_deportivas',
        'datos': participaciones,
        'visualizaciones': visualizaciones,
        'form': form,
    })