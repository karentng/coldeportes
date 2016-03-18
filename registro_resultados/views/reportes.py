from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from datetime import datetime
from django.template import RequestContext
from entidades.models import *
from django.http import JsonResponse,HttpResponse
from registro_resultados.models import *
from registro_resultados.forms import *
from django.db.models import F, Count


def cambiarEtiquetasPosiciones(medallas):
    auxiliar_medallas = dict()
    for key, value in medallas.items():
        if key == 1:
            auxiliar_medallas[("%s")%("Oro")] = value
        elif key == 2:
            auxiliar_medallas[("%s")%("Plata")] = value
        elif key == 3:
            auxiliar_medallas[("%s")%("Bronce")] = value

    return auxiliar_medallas

@login_required
def medalleria_genero(request):
    """
    Marzo 10, 2015
    Autor: Karent Narvaez

    Permite conocer el numero de medallas de acuerdo al departamento y género.
    """
    from reportes.utilities import sumar_datos_diccionario
    from coldeportes.utilities import get_request_or_none

    tipoTenant = request.tenant.obtenerTenant()

    if request.is_ajax():
        departamentos = get_request_or_none(request.GET, 'departamentos')
        generos = get_request_or_none(request.GET, 'generos')    
    

        #Departamentos, Generos
        if departamentos and generos:
            medallas = Participante.objects.filter(posicion__in=[1,2,3], departamento__in=departamentos, genero__in=generos).annotate(descripcion=F('posicion')).values('id', 'descripcion').annotate(cantidad=Count('id', distinct=True))
        #Departamentos
        elif departamentos:

            medallas = Participante.objects.filter(posicion__in=[1,2,3], departamento__in=departamentos).annotate(descripcion=F('posicion')).values('id', 'descripcion').annotate(cantidad=Count('id', distinct=True))
        #Generos
        elif generos:
            medallas = Participante.objects.filter(posicion__in=[1,2,3], genero__in=generos).annotate(descripcion=F('posicion')).values('id', 'descripcion').annotate(cantidad=Count('id', distinct=True))
        #Sin filtros
        else:
            medallas = Participante.objects.filter(posicion__in=[1,2,3]).annotate(descripcion=F('posicion')).values('id', 'descripcion').annotate(cantidad=Count('id', distinct=True))

        
        medallas = tipoTenant.ajustar_resultado(medallas)
        medallas = cambiarEtiquetasPosiciones(medallas)
        

        return JsonResponse(medallas)

    else:
        medallas = list(Participante.objects.filter(posicion__in=[1,2,3]).annotate(descripcion=F('posicion')).values('descripcion', 'departamento').annotate(cantidad=Count('id')))

        medallas = tipoTenant.ajustar_resultado(medallas)

    medallas = cambiarEtiquetasPosiciones(medallas)

    #print(medallas)
    visualizaciones = [1, 5 , 6]
    form = FiltrosMedalleriaDeptGenForm(visualizaciones=visualizaciones)    
    nombres_columnas = ["Medallas", "Departamento"]

    return render(request, 'reportes/medalleria_genero.html', {
        'nombre_reporte' : 'Medallería por Género',
        'tres_filtros': True,
        'url_data' : 'reporte_medalleria_genero',
        'datos': medallas,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Registro de Resultados',
        'fecha_generado': datetime.now(),
        'nombres_columnas': nombres_columnas

    })
