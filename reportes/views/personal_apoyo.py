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
    """
    Noviembre 13, 2015
    Autor: Daniel Correa

    Permite ejecutar los diferentes filtros de casos de acuerdo a un arreglo de consultas
    CONSULTAS LLEVA EL SIGUIENTE FORMATO [contulta caso 1, consulta caso 2 , consulta caso 3, ... ,consulta caso n]
    LOS CASOS EMPIEZAN EN 1 EL DE MAS ARRIBA HASTA N EL DE MAS ABAJO
    """
    if departamentos and genero:
        try:
            resultado = eval(consultas[0]%(departamentos,genero))
        except Exception as e:
            print(e)
    elif departamentos:
        try:
            resultado = eval(consultas[1]%(departamentos))
        except Exception as e:
            print(e)
    elif genero:
        try:
            resultado = eval(consultas[2]%(genero))
        except Exception as e:
            print(e)
    else:
        try:
            resultado = eval(consultas[3])
        except Exception as e:
            print(e)
    return resultado


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
    return render(request,'personal_apoyo/base_personal_apoyo.html',{
        'nombre_reporte' : 'Actividades que desempeña el personal de apoyo',
        'url_data' : 'reporte_actividades_personal',
        'datos': datos,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Personal de Apoyo',
        'fecha_generado': datetime.now(),
        'nombre_columna':'Actividad'
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
        formaciones = tipoTenant.ajustar_resultado(formaciones)
        return JsonResponse(formaciones)

    else:
        formaciones = list(tabla.objects.filter(estado=0,estado_formacion='Finalizado').annotate(descripcion=F('nivel_formacion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        formaciones = tipoTenant.ajustar_resultado(formaciones)

    visualizaciones = [1, 2, 3, 5, 6, 7]
    form = FiltrosPersonalApoyoForm(visualizaciones=visualizaciones)
    return render(request, 'personal_apoyo/base_personal_apoyo.html', {
        'nombre_reporte' : 'Formación académica del personal de apoyo',
        'url_data' : 'reporte_formacion_academica_personal',
        'datos': formaciones,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Personal de Apoyo',
        'fecha_generado': datetime.now(),
        'nombre_columna':'Nivel de Formación'
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
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad__departamento__id__in=%s,genero__in=%s).values('id','entidad').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad__departamento__id__in=%s).values('id','entidad').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,genero__in=%s).values('id','entidad').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0).values('id','entidad').annotate(cantidad=Count('id',distinct=True)))",
        ]

        total_personal = len(ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant))

        resultado = {
            'Total Personal de Apoyo':total_personal
        }

        return JsonResponse(resultado)

    else:
        total_personal = len(tabla.objects.filter(estado = 0).values('id','entidad').annotate(cantidad=Count('id',distinct=True)))
        resultado = {
            'Total Personal de Apoyo':total_personal
        }

    visualizaciones = [1, 2, 3, 5, 6, 7]
    form = FiltrosPersonalApoyoForm(visualizaciones=visualizaciones)
    return render(request, 'personal_apoyo/base_personal_apoyo.html', {
        'nombre_reporte' : 'Cantidad total de personal de apoyo',
        'url_data' : 'reporte_cantidad_total_personal_apoyo',
        'datos': resultado,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Personal de Apoyo',
        'fecha_generado': datetime.now(),
        'nombre_columna':'Descripción'
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
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad__departamento__id__in=%s).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,genero__in=%s).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
        ]

        lgtbi = ejecutar_casos_recursivos(consultas, departamentos, genero, tipoTenant)
        lgtbi = tipoTenant.ajustar_resultado(lgtbi)
        if True in lgtbi:
            lgtbi['PERTENECE A LA COMUNIDAD LGTBI'] = lgtbi[True]
            del lgtbi[True]
        if False in lgtbi:
            lgtbi['NO PERTENECE A LA COMUNIDAD LGTBI'] = lgtbi[False]
            del lgtbi[False]

        return JsonResponse(lgtbi)

    else:
        lgtbi = list(tabla.objects.filter(estado = 0).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        lgtbi = tipoTenant.ajustar_resultado(lgtbi)
        print(lgtbi)
        if True in lgtbi:
            lgtbi['PERTENECE A LA COMUNIDAD LGTBI'] = lgtbi[True]
            del lgtbi[True]
        if False in lgtbi:
            lgtbi['NO PERTENECE A LA COMUNIDAD LGTBI'] = lgtbi[False]
            del lgtbi[False]

    visualizaciones = [1, 2, 3, 5, 6]
    form = FiltrosPersonalApoyoForm(visualizaciones=visualizaciones)

    return render(request, 'personal_apoyo/base_personal_apoyo.html', {
        'nombre_reporte' : 'Cantidad de personal de apoyo que pertenece a la comunidad LGTBI',
        'url_data' : 'reporte_lgtbi_personal_apoyo',
        'datos': lgtbi,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Personal de Apoyo',
        'fecha_generado': datetime.now(),
        'nombre_columna':'Descripción'
    })

def reporte_etnias(request):
    """
    Enero 23, 2016
    Autor: Cristian Leonardo Ríos López

    Permite conocer el numero de personal de apoyo agrupado por etnias
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
            "list("+tabla.__name__+".objects.filter(estado=0,ciudad__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('etnia')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,ciudad__departamento__id__in=%s).annotate(descripcion=F('etnia')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,genero__in=%s).annotate(descripcion=F('etnia')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0).annotate(descripcion=F('etnia')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
        ]

        etnias = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)
        etnias = tipoTenant.ajustar_resultado(etnias)

        if '' in etnias:
            etnias['Ninguna'] = etnias['']
            del etnias['']

        return JsonResponse(etnias)

    else:
        etnias = list(tabla.objects.filter(estado=0).annotate(descripcion=F('etnia')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        etnias = tipoTenant.ajustar_resultado(etnias)

        if '' in etnias:
            etnias['NO APLICA'] = etnias['']
            del etnias['']

    visualizaciones = [1, 2, 3, 5]
    form = FiltrosPersonalApoyoForm(visualizaciones=visualizaciones)
    return render(request, 'personal_apoyo/base_personal_apoyo.html', {
        'nombre_reporte' : 'Etnias del personal de apoyo',
        'url_data' : 'reporte_etnias_personal_apoyo',
        'datos': etnias,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Personal de Apoyo',
        'fecha_generado': datetime.now(),
        'nombres_columna':'Etnia'
    })
