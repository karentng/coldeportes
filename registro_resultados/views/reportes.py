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
        juegos = get_request_or_none(request.GET, 'juegos')
    
        if juegos:
            #Departamentos, Generos
            if departamentos and generos:
                medallas = Participante.objects.filter(posicion__in=[1,2,3], departamento__in=departamentos, genero__in=generos, competencia__juego=juegos).annotate(descripcion=F('posicion')).values('id', 'descripcion').annotate(cantidad=Count('id', distinct=True))
            #Departamentos
            elif departamentos:

                medallas = Participante.objects.filter(posicion__in=[1,2,3], departamento__in=departamentos, competencia__juego=juegos).annotate(descripcion=F('posicion')).values('id', 'descripcion').annotate(cantidad=Count('id', distinct=True))
            #Generos
            elif generos:
                medallas = Participante.objects.filter(posicion__in=[1,2,3], genero__in=generos, competencia__juego=juegos).annotate(descripcion=F('posicion')).values('id', 'descripcion').annotate(cantidad=Count('id', distinct=True))
            #Sin filtros
            else:
                medallas = Participante.objects.filter(posicion__in=[1,2,3], competencia__juego=juegos).annotate(descripcion=F('posicion')).values('id', 'descripcion').annotate(cantidad=Count('id', distinct=True))

            
            medallas = tipoTenant.ajustar_resultado(medallas)
            medallas = cambiarEtiquetasPosiciones(medallas)
            

            return JsonResponse(medallas)
        else:
            #print('seleccione un juego')
            pass

    else:
        medallas = list(Participante.objects.filter(posicion__in=[1,2,3]).annotate(descripcion=F('posicion')).values('descripcion', 'departamento').annotate(cantidad=Count('id')))

        medallas = tipoTenant.ajustar_resultado(medallas)

    medallas = cambiarEtiquetasPosiciones(medallas)

    visualizaciones = [1, 5 , 6]
    form = FiltrosMedalleriaDeptGenForm(visualizaciones=visualizaciones)    
    nombres_columnas = ["Medallas", "Departamento"]

    return render(request, 'reportes/medalleria_genero.html', {
        'nombre_reporte' : 'Medallería de Juegos por Género y Departamento',
        'url_data' : 'reporte_medalleria_genero',
        'datos': medallas,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Registro de Resultados',
        'fecha_generado': datetime.now(),
        'nombres_columnas': nombres_columnas

    })


def contar_registros(consulta):

    consulta = consulta.values('departamento').annotate(cantidad = Count('id'))
    cantidades = { int(entry['departamento']) : entry['cantidad'] for entry in consulta }
    return cantidades


def verificar_agrupar_listas_por_departamento(lista1, lista2):
    #print(lista1)
    #print(lista2)
    for departamento in lista1:
        if lista2.get(departamento):
            lista2[departamento] += lista1.get(departamento)
        else:
            lista2[departamento] = lista1.get(departamento)
    #print(lista2)
    return lista2


def buscar_medallas_por_categoria(posicion, genero=None):

    if genero:
        medallas_participante = contar_registros(Participante.objects.filter(posicion__in=[posicion], genero=genero))
        medallas_equipo = contar_registros(Equipo.objects.filter(posicion__in=[posicion], genero=genero))
        medallas = verificar_agrupar_listas_por_departamento(medallas_participante, medallas_equipo)
    else:
        medallas_participante = contar_registros(Participante.objects.filter(posicion__in=[posicion]))
        medallas_equipo = contar_registros(Equipo.objects.filter(posicion__in=[posicion]))
        medallas = verificar_agrupar_listas_por_departamento(medallas_participante, medallas_equipo)

    return medallas

def buscar_medallas_totales(juego, deporte):

    if deporte:
        pass
    else:
        pass



@login_required
def tabla_medalleria(request):

    total_medallas_general = 0
    resultados = list()

    #Buscar totales sin género 
    medallas_oro = buscar_medallas_por_categoria(1)
    medallas_plata = buscar_medallas_por_categoria(2)
    medallas_bronce = buscar_medallas_por_categoria(3)
    #Buscar totales femenino
    medallas_oro_femenino = buscar_medallas_por_categoria(1, 'MUJER')
    medallas_plata_femenino = buscar_medallas_por_categoria(2, 'MUJER')
    medallas_bronce_femenino = buscar_medallas_por_categoria(3, 'MUJER')
    #Buscar totales masculino
    medallas_oro_masculino = buscar_medallas_por_categoria(1, 'HOMBRE')
    medallas_plata_masculino = buscar_medallas_por_categoria(1, 'HOMBRE')
    medallas_bronce_masculino = buscar_medallas_por_categoria(1, 'HOMBRE')
    #Buscar totales mixto
    medallas_oro_mixto = buscar_medallas_por_categoria(1, 'MIXTO')
    medallas_plata_mixto = buscar_medallas_por_categoria(1, 'MIXTO')
    medallas_bronce_mixto = buscar_medallas_por_categoria(1, 'MIXTO')


    for departamento in Departamento.objects.all():
        if departamento.id in medallas_oro or departamento.id in medallas_plata or departamento.id in medallas_bronce:

            departamento.total_oro = medallas_oro.get(departamento.id, 0)
            departamento.total_plata = medallas_plata.get(departamento.id, 0)
            departamento.total_bronce = medallas_bronce.get(departamento.id, 0)
            departamento.total_medallas = departamento.total_oro + departamento.total_plata + departamento.total_bronce

            departamento.total_oro_femenino = medallas_oro_femenino.get(departamento.id, 0)
            departamento.total_plata_femenino = medallas_plata_femenino.get(departamento.id, 0)
            departamento.total_bronce_femenino = medallas_bronce_femenino.get(departamento.id, 0)
            departamento.total_medallas_femenino = departamento.total_oro_femenino + departamento.total_plata_femenino + departamento.total_bronce_femenino

            departamento.total_oro_masculino = medallas_oro_masculino.get(departamento.id, 0)
            departamento.total_plata_masculino = medallas_plata_masculino.get(departamento.id, 0)
            departamento.total_bronce_masculino = medallas_bronce_masculino.get(departamento.id, 0)
            departamento.total_medallas_masculino = departamento.total_oro_masculino + departamento.total_plata_masculino + departamento.total_bronce_masculino 

            departamento.total_oro_mixto = medallas_oro_mixto.get(departamento.id, 0)
            departamento.total_plata_mixto = medallas_plata_mixto.get(departamento.id, 0)
            departamento.total_bronce_mixto = medallas_bronce_mixto.get(departamento.id, 0)
            departamento.total_medallas_mixto = departamento.total_oro_mixto + departamento.total_plata_mixto + departamento.total_bronce_mixto            
            
            total_medallas_general += departamento.total_medallas
            resultados.append(departamento)


    return render(request, 'reportes/tabla_medalleria.html', {
        'resultados': resultados,
        'total_medallas': total_medallas_general,
        
        })


