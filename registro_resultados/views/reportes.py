from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from datetime import datetime
from django.template import RequestContext
from entidades.models import *
from django.http import JsonResponse,HttpResponse
from registro_resultados.models import *
from registro_resultados.forms import *

@login_required
def medalleria_genero(request):
    """
    Marzo 10, 2015
    Autor: Karent Narvaez

    Permite conocer el numero de medallas de acuerdo al departamento y género.
    """

    if request.is_ajax():
        departamentos = get_request_or_none(request.GET, 'departamentos')
        generos = get_request_or_none(request.GET, 'generos')    
        return JsonResponse(escenarios)


    visualizaciones = [1, 5 , 6]

    form = FiltrosMedalleriaDeptGenForm(visualizaciones=visualizaciones)
    nombres_columnas = ["Clase", "Caracteristica", "Comuna"]
    return render(request, 'escenarios/reporte_generador.html', {
        'nombre_reporte' : 'Clase de Acceso Escenarios',
        'nombre_generador': 'Características Escenarios',
        'url_data' : 'reportes_caracteristicas_escenarios',
        #'datos': medallas,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Escenarios',
        'fecha_generado': datetime.now(),
        'nombres_columnas': nombres_columnas

    })
