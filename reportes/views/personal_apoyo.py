#encoding:utf-8
from django.http import JsonResponse
from django.shortcuts import render, redirect
from entidades.modelos_vistas_reportes import PublicPersonalApoyoView
from reportes.models import TenantPersonalApoyoView
from reportes.forms import FiltrosPersonalApoyoForm
from django.db.models import F, Count
from reportes.utilities import sumar_datos_diccionario, convert_choices_to_array, crear_diccionario_inicial
from snd.models import PersonalApoyo
import ast


def ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant):

    if departamentos and genero:
        participaciones = eval(consultas[0]%(departamentos,genero))
    elif departamentos:
        participaciones = eval(consultas[1]%(departamentos))
    elif genero:
        participaciones = eval(consultas[2]%(genero))
    else:
        participaciones = eval(consultas[3])
    participaciones = tipoTenant.ajustar_resultado(participaciones)
    return participaciones


def reporte_actividades_personal(request):
    """
    Noviembre 19, 2015
    Autor: Milton Lenis

    Reporte actividades del personal de apoyo:
    En esta vista se manejan todos los filtros y consultas para generar los datos para el reporte de las actividades que
    desempeña el personal de apoyo
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicPersonalApoyoView
    else:
        tabla = TenantPersonalApoyoView

    if request.is_ajax():

        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        consultas = [
            "list("+tabla.__name__+".objects.filter(ciudad__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('actividad')).values('id','descripcion').annotate(cantidad=Count('descripcion', distinct=True)))",
            "list("+tabla.__name__+".objects.filter(ciudad__departamento__id__in=%s).annotate(descripcion=F('actividad')).values('id','descripcion').annotate(cantidad=Count('descripcion', distinct=True)))",
            "list("+tabla.__name__+".objects.filter(genero__in=%s).annotate(descripcion=F('actividad')).values('id','descripcion').annotate(cantidad=Count('descripcion', distinct=True)))",
            "list("+tabla.__name__+".objects.annotate(descripcion=F('actividad')).values('id','descripcion').annotate(cantidad=Count('descripcion', distinct=True)))",
        ]

        datos = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)

        return JsonResponse(datos)

    else:
        datos = list(tabla.objects.annotate(descripcion=F('actividad')).values('id','descripcion').annotate(cantidad=Count('descripcion', distinct=True)))
        #datos = tipoTenant.ajustar_resultado(datos)
        datos = sumar_datos_diccionario(datos, PersonalApoyo.ACTIVIDADES)


    visualizaciones = [1, 2, 3, 5, 6, 7]
    form = FiltrosPersonalApoyoForm(visualizaciones=visualizaciones)
    return render(request,'base_reportes.html',{
        'nombre_reporte' : 'Actividades que desempeña el personal de apoyo',
        'url_data' : 'reporte_actividades_personal',
        'datos': datos,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Personal de Apoyo'
    })

