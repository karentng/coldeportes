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
from datetime import datetime


def ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant):

    if departamentos and genero:
        participaciones = eval(consultas[0]%(departamentos,genero))
    elif departamentos:
        participaciones = eval(consultas[1]%(departamentos))
    elif genero:
        participaciones = eval(consultas[2]%(genero))
    else:
        participaciones = eval(consultas[3])
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
        datos = sumar_datos_diccionario(datos,PersonalApoyo.ACTIVIDADES)

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


def reporte_formacion_academica_personal(request):
    """
    Diciembre 21, 2015
    Autor: Milton Lenis

    Permite conocer la formacion academica del personal de apoyo caracterizada por niveles de formación
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
            "list("+tabla.__name__+".objects.filter(estado=0,estado_formacion='Finalizado',ciudad__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('nivel_formacion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,estado_formacion='Finalizado',ciudad__departamento__id__in=%s).annotate(descripcion=F('nivel_formacion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,estado_formacion='Finalizado',genero__in=%s).annotate(descripcion=F('nivel_formacion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,estado_formacion='Finalizado').annotate(descripcion=F('nivel_formacion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
        ]

        formaciones = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)

        return JsonResponse(formaciones)

    else:
        formaciones = list(tabla.objects.filter(estado=0,estado_formacion='Finalizado').annotate(descripcion=F('nivel_formacion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        formaciones = tipoTenant.ajustar_resultado(formaciones)

    visualizaciones = [1, 2, 3, 5, 6, 7]
    form = FiltrosPersonalApoyoForm(visualizaciones=visualizaciones)
    return render(request, 'base_reportes.html', {
        'nombre_reporte' : 'Formación Academica del personal de apoyo',
        'url_data' : 'reporte_formacion_academica_personal',
        'datos': formaciones,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Personal de Apoyo',
        'fecha_generado': datetime.now()
    })


def reporte_cantidad_total_personal_apoyo(request):
    """
    Diciembre 21, 2015
    Autor: Milton Lenis

    Permite conocer el número total de personal de apoyo
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicPersonalApoyoView
    else:
        tabla = TenantPersonalApoyoView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null' else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        consultas = [
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s,genero__in=%s).order_by('id').distinct('id'))",
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s).order_by('id').distinct('id'))",
            "list("+tabla.__name__+".objects.filter(estado = 0,genero__in=%s).order_by('id').distinct('id'))",
            "list("+tabla.__name__+".objects.filter(estado = 0).order_by('id').distinct('id'))",
        ]

        total_personal = len(ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant))

        resultado = {
            'Total Personal de Apoyo':total_personal
        }

        return JsonResponse(resultado)

    else:
        total_personal = len(tabla.objects.filter(estado = 0).order_by('id').distinct('id'))

        resultado = {
            'Total Personal de Apoyo':total_personal
        }

    visualizaciones = [1, 2, 3, 5, 6, 7]
    form = FiltrosPersonalApoyoForm(visualizaciones=visualizaciones)
    return render(request, 'base_reportes.html', {
        'nombre_reporte' : 'Cantidad TOTAL de personal de apoyo',
        'url_data' : 'reporte_cantidad_total_personal_apoyo',
        'datos': resultado,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Personal de Apoyo',
        'fecha_generado': datetime.now()
    })

def reporte_lgtbi(request):
    """
    Diciembre 21, 2015
    Autor: Milton Lenis

    Permite conocer el numero de personal de apoyo que pertenecen a la comunidad LGTBI
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
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,genero__in=%s).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
        ]

        lgbti = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)
        if True in lgbti:
            lgbti['Pertenece a la comunidad LGTBI'] = lgbti[True]
            del lgbti[True]
        if False in lgbti:
            lgbti['No pertenece a la comunidad LGTBI'] = lgbti[False]
            del lgbti[False]

        return JsonResponse(lgtbi)

    else:
        lgtbi = list(tabla.objects.filter(estado = 0).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        lgtbi = tipoTenant.ajustar_resultado(lgtbi)

        if True in lgtbi:
            lgtbi['Usa centros biomédicos'] = lgtbi[True]
            del lgtbi[True]
        if False in lgtbi:
            lgtbi['No usa centros biomédicos'] = lgtbi[False]
            del lgtbi[False]

    visualizaciones = [1, 2, 3, 5, 6, 7]
    form = FiltrosPersonalApoyoForm(visualizaciones=visualizaciones)

    return render(request, 'base_reportes.html', {
        'nombre_reporte' : 'Personal de Apoyo que pertenece a la comunidad LGTBI',
        'url_data' : 'reporte_lgtbi_personal_apoyo',
        'datos': lgtbi,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Personal de Apoyo',
        'fecha_generado': datetime.now()
    })
