#encoding:utf-8
from django.http import JsonResponse
from django.shortcuts import render, redirect
from entidades.modelos_vistas_reportes import PublicPersonalApoyoView
from reportes.models import TenantPersonalApoyoView
from reportes.forms import FiltrosPersonalApoyoForm
from django.db.models import F, Count
from reportes.utilities import sumar_datos_diccionario, convert_choices_to_array
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

    valores_choices = convert_choices_to_array(PersonalApoyo.ACTIVIDADES)

    #Valores del choices del modelo equivalentes a los números que ocupan el diccionario como llaves
    """valores_choices = ['MÉDICO DEPORTÓLOGO', 'FISIOTERAPEUTA', 'PSICÓLOGO DEPORTIVO', 'NUTRICIONISTA', 'QUINESIÓLOGO',
                       'QUIROPRÁCTICO', 'PREPARADOR FÍSICO', 'TRABAJADOR SOCIAL', 'FISIÓLOGO', 'BIOMECÁNICO',
                       'METODÓLOGO', 'ENTRENADOR', 'MONITOR', 'ENTRENADOR PERSONALIZADO', 'ANIMADOR SOCIOCULTURAL',
                       'RECREADOR', 'PROMOTOR DE ACTIVIDAD FÍSICA']"""
    #Inicializamos los datos, los números de la izquierda significan el valor real representado en la base de datos para
    #cada una de las categorías, este valor se saca así de las consultas.
    datos_iniciales = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
        13: 0,
        14: 0,
        15: 0,
        16: 0,
    }

    if request.is_ajax():
        datos = list(tabla.objects.annotate(descripcion=F('actividad')).values('id','descripcion').annotate(cantidad=Count('descripcion', distinct=True)))
        datos = tipoTenant.ajustar_resultado(datos)

        return JsonResponse(datos)
    else:
        datos = list(tabla.objects.annotate(descripcion=F('actividad')).values('id','descripcion').annotate(cantidad=Count('descripcion', distinct=True)))
        #datos = tipoTenant.ajustar_resultado(datos)
        datos = sumar_datos_diccionario(datos_iniciales, datos, valores_choices)


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

