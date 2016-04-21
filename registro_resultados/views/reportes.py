from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from datetime import datetime
from django.template import RequestContext
from entidades.models import *
from django.http import JsonResponse, HttpResponse
from registro_resultados.models import *
from registro_resultados.forms import *
from django.db.models import F, Count
from coldeportes.utilities import get_request_or_none


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

    for departamento in lista1:
        if lista2.get(departamento):
            lista2[departamento] += lista1.get(departamento)
        else:
            lista2[departamento] = lista1.get(departamento)

    return lista2


def buscar_medallas_por_categoria(posicion, juego, deportes=None, genero=None):

    if deportes:
        if genero:
            medallas_participante = contar_registros(Participante.objects.filter(posicion__in=[posicion], genero=genero, competencia__juego=juego, competencia__deporte__in=deportes))
            medallas_equipo = contar_registros(Equipo.objects.filter(posicion__in=[posicion], genero=genero, competencia__juego=juego, competencia__deporte__in=deportes))
            medallas = verificar_agrupar_listas_por_departamento(medallas_participante, medallas_equipo)
        else:
            medallas_participante = contar_registros(Participante.objects.filter(posicion__in=[posicion], competencia__juego=juego, competencia__deporte__in=deportes))
            medallas_equipo = contar_registros(Equipo.objects.filter(posicion__in=[posicion], competencia__juego=juego, competencia__deporte__in=deportes))
            medallas = verificar_agrupar_listas_por_departamento(medallas_participante, medallas_equipo)
    else:
        if genero:
            medallas_participante = contar_registros(Participante.objects.filter(posicion__in=[posicion], genero=genero, competencia__juego=juego))
            medallas_equipo = contar_registros(Equipo.objects.filter(posicion__in=[posicion], genero=genero, competencia__juego=juego))
            medallas = verificar_agrupar_listas_por_departamento(medallas_participante, medallas_equipo)
        else:
            medallas_participante = contar_registros(Participante.objects.filter(posicion__in=[posicion], competencia__juego=juego))
            medallas_equipo = contar_registros(Equipo.objects.filter(posicion__in=[posicion], competencia__juego=juego))
            medallas = verificar_agrupar_listas_por_departamento(medallas_participante, medallas_equipo)
        #print(medallas)

    return medallas


def buscar_medallas_totales(juego, deportes):

    resultados = dict()

    #Buscar totales sin género 
    resultados['medallas_oro'] = buscar_medallas_por_categoria(1, juego, deportes)
    resultados['medallas_plata'] = buscar_medallas_por_categoria(2, juego, deportes)
    resultados['medallas_bronce'] = buscar_medallas_por_categoria(3, juego, deportes)
    #Buscar totales masculino
    resultados['medallas_oro_masculino'] = buscar_medallas_por_categoria(1, juego, deportes, 1)
    resultados['medallas_plata_masculino'] = buscar_medallas_por_categoria(2, juego, deportes, 1)
    resultados['medallas_bronce_masculino'] = buscar_medallas_por_categoria(3, juego, deportes, 1)
    #Buscar totales femenino
    resultados['medallas_oro_femenino'] = buscar_medallas_por_categoria(1, juego, deportes, 2)
    resultados['medallas_plata_femenino'] = buscar_medallas_por_categoria(2, juego, deportes, 2)
    resultados['medallas_bronce_femenino'] = buscar_medallas_por_categoria(3, juego, deportes, 2)
    #Buscar totales mixto
    resultados['medallas_oro_mixto'] = buscar_medallas_por_categoria(1, juego, deportes, 3)
    resultados['medallas_plata_mixto'] = buscar_medallas_por_categoria(2, juego, deportes, 3)
    resultados['medallas_bronce_mixto'] = buscar_medallas_por_categoria(3, juego, deportes, 3)

    return resultados


@login_required
def tabla_medalleria(request):

    """
    Abril 4, 2015
    Autor: Karent Narvaez

    Tabla que permite conocer el numero de medallas de acuerdo al juego, departamento, género y deporte.
    """
    form = FiltrosTablaMedalleriaForm()    
    total_medallas_general = 0
    resultados = list()
    filtros = False

    if request.method == 'POST':

        form = FiltrosTablaMedalleriaForm(request.POST)  

        if form.is_valid():  

            deportes = request.POST.getlist('deportes') or None   
            juego = request.POST.get('juego') or None
            medalleria = buscar_medallas_totales(juego, deportes)
            filtros = True

            for departamento in Departamento.objects.all():
                if departamento.id in medalleria['medallas_oro'] or departamento.id in medalleria['medallas_plata'] or departamento.id in medalleria['medallas_bronce']:

                    departamento.total_oro = medalleria['medallas_oro'].get(departamento.id, 0)
                    departamento.total_plata = medalleria['medallas_plata'].get(departamento.id, 0)
                    departamento.total_bronce = medalleria['medallas_bronce'].get(departamento.id, 0)
                    departamento.total_medallas = departamento.total_oro + departamento.total_plata + departamento.total_bronce
                    
                    departamento.total_oro_femenino = medalleria['medallas_oro_femenino'].get(departamento.id, 0)
                    departamento.total_plata_femenino = medalleria['medallas_plata_femenino'].get(departamento.id, 0)
                    departamento.total_bronce_femenino = medalleria['medallas_bronce_femenino'].get(departamento.id, 0)
                    departamento.total_medallas_femenino = departamento.total_oro_femenino + departamento.total_plata_femenino + departamento.total_bronce_femenino

                    departamento.total_oro_masculino = medalleria['medallas_oro_masculino'].get(departamento.id, 0)
                    departamento.total_plata_masculino = medalleria['medallas_plata_masculino'].get(departamento.id, 0)
                    departamento.total_bronce_masculino = medalleria['medallas_bronce_masculino'].get(departamento.id, 0)
                    departamento.total_medallas_masculino = departamento.total_oro_masculino + departamento.total_plata_masculino + departamento.total_bronce_masculino 

                    departamento.total_oro_mixto = medalleria['medallas_oro_mixto'].get(departamento.id, 0)
                    departamento.total_plata_mixto = medalleria['medallas_plata_mixto'].get(departamento.id, 0)
                    departamento.total_bronce_mixto = medalleria['medallas_bronce_mixto'].get(departamento.id, 0)
                    departamento.total_medallas_mixto = departamento.total_oro_mixto + departamento.total_plata_mixto + departamento.total_bronce_mixto            
                    
                    total_medallas_general += departamento.total_medallas
                    resultados.append(departamento)

    return render(request, 'reportes/tabla_medalleria.html', {
        'resultados': resultados,
        'total_medallas': total_medallas_general,
        'form': form,
        'filtros': filtros,
        'url_data' : 'reporte_tabla_medalleria',
    })
