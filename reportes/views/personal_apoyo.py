#encoding:utf-8
from django.http import JsonResponse
from django.shortcuts import render, redirect
from entidades.modelos_vistas_reportes import PublicPersonalApoyoView
from reportes.models import TenantPersonalApoyoView
from reportes.forms import FiltrosPersonalApoyoForm
from django.db.models import F, Count
from reportes.utilities import sumar_datos_diccionario, convert_choices_to_array, crear_diccionario_inicial
from snd.models import PersonalApoyo


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
        datos = list(tabla.objects.annotate(descripcion=F('actividad')).values('id','descripcion').annotate(cantidad=Count('descripcion', distinct=True)))
        datos = tipoTenant.ajustar_resultado(datos)

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

