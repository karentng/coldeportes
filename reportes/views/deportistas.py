#encoding:utf-8
from django.shortcuts import render, redirect
from snd.modelos.deportistas import HistorialDeportivo,Deportista,InformacionAdicional,Deportista,InformacionAcademica
from entidades.models import Departamento
from django.db.models import Count
from reportes.forms import FiltrosDeportistasForm
from django.db.models import F
import ast
from datetime import datetime
from django.http import JsonResponse
from entidades.modelos_vistas_reportes import PublicDeportistaView
from reportes.models import TenantDeportistaView

def ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant):
    """
    Noviembre 13, 2015
    Autor: Daniel Correa

    Permite ejecutar los diferentes filtros de casos de acuerdo a un arreglo de consultas
    CONSULTAS LLEVA EL SIGUIENTE FORMATO [contulta caso 1, consulta caso 2 , consulta caso 3, ... ,consulta caso n]
    LOS CASOS EMPIEZAN EN 1 EL DE MAS ARRIBA HASTA N EL DE MAS ABAJO
    """
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

def participaciones_deportivas(request):
    """
    Noviembre 13, 2015
    Autor: Daniel Correa

    Reporte participaciones deportivas:
    Consulta que trae el numero de  participaciones deportiva ordenadas por tipo
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicDeportistaView
    else:
        tabla = TenantDeportistaView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        consultas = [
            "list("+tabla.__name__+".objects.filter(estado = 0,estado_participacion='Aprobado',ciudad_residencia__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('tipo_participacion')).values('descripcion').annotate(cantidad=Count('tipo_participacion')))",
            "list("+tabla.__name__+".objects.filter(estado = 0,estado_participacion='Aprobado',ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('tipo_participacion')).values('descripcion').annotate(cantidad=Count('tipo_participacion')))",
            "list("+tabla.__name__+".objects.filter(estado = 0,estado_participacion='Aprobado',genero__in=%s).annotate(descripcion=F('tipo_participacion')).values('descripcion').annotate(cantidad=Count('tipo_participacion')))",
            "list("+tabla.__name__+".objects.filter(estado = 0,estado_participacion='Aprobado').annotate(descripcion=F('tipo_participacion')).values('descripcion').annotate(cantidad=Count('tipo_participacion')))"
        ]

        participaciones = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)

        return JsonResponse(participaciones)

    else:
        #Traer la cantidad de hisotriales ordenados por tipo
        participaciones = list(tabla.objects.filter(estado = 0,estado_participacion="Aprobado").annotate(descripcion=F('tipo_participacion')).values('descripcion').annotate(cantidad=Count('tipo_participacion')))
        participaciones = tipoTenant.ajustar_resultado(participaciones)

    visualizaciones = [1, 2, 3, 5, 6, 7]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Participaciones Deportivas',
        'url_data' : 'reporte_participaciones_deportivas',
        'datos': participaciones,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now()
    })

def beneficiario_programa_apoyo(request):
    """
    Noviembre 13, 2015
    Autor: Daniel Correa

    Permite conocer el numero de deportistas beneficiados por un programa de apoyo
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicDeportistaView
    else:
        tabla = TenantDeportistaView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        consultas = [
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('es_beneficiario_programa_apoyo')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('es_beneficiario_programa_apoyo')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,genero__in=%s).annotate(descripcion=F('es_beneficiario_programa_apoyo')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0).annotate(descripcion=F('es_beneficiario_programa_apoyo')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
        ]

        beneficiados = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)
        if True in beneficiados:
            beneficiados['Deportistas beneficiados'] = beneficiados[True]
            del beneficiados[True]
        if False in beneficiados:
            beneficiados['Deportistas no beneficiados'] = beneficiados[False]
            del beneficiados[False]

        return JsonResponse(beneficiados)

    else:
        beneficiados = list(tabla.objects.filter(estado = 0).annotate(descripcion=F('es_beneficiario_programa_apoyo')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        beneficiados = tipoTenant.ajustar_resultado(beneficiados)

        if True in beneficiados:
            beneficiados['Deportistas beneficiados'] = beneficiados[True]
            del beneficiados[True]
        if False in beneficiados:
            beneficiados['Deportistas no beneficiados'] = beneficiados[False]
            del beneficiados[False]

    visualizaciones = [1, 2, 3, 5, 6]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Beneficiario Programa de Apoyo',
        'url_data' : 'reporte_beneficiario_programa_apoyo',
        'datos': beneficiados,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now()
    })

def etinias_deportistas(request):
    """
    Noviembre 13, 2015
    Autor: Daniel Correa

    Permite conocer el numero de deportistas ordenados por etnias
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicDeportistaView
    else:
        tabla = TenantDeportistaView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        consultas = [
            "list("+tabla.__name__+".objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('etnia')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('etnia')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,genero__in=%s).annotate(descripcion=F('etnia')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0).annotate(descripcion=F('etnia')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
        ]

        etnias = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)

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
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Etnias de los deportistas',
        'url_data' : 'reporte_etinias_deportistas',
        'datos': etnias,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now()
    })

def formacion_academica(request):
    """
    Noviembre 14, 2015
    Autor: Daniel Correa

    Permite conocer la formacion academica de los deportistas caracterizadas por niveles de formacion
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicDeportistaView
    else:
        tabla = TenantDeportistaView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        consultas = [
            "list("+tabla.__name__+".objects.filter(estado=0,estado_formacion='Finalizado',ciudad_residencia__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('nivel_formacion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,estado_formacion='Finalizado',ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('nivel_formacion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,estado_formacion='Finalizado',genero__in=%s).annotate(descripcion=F('nivel_formacion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,estado_formacion='Finalizado').annotate(descripcion=F('nivel_formacion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
        ]

        formaciones = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)

        return JsonResponse(formaciones)

    else:
        formaciones = list(tabla.objects.filter(estado=0,estado_formacion='Finalizado').annotate(descripcion=F('nivel_formacion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        formaciones = tipoTenant.ajustar_resultado(formaciones)

    visualizaciones = [1, 2, 3, 5, 6, 7]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Formación Academica de los deportistas',
        'url_data' : 'reporte_formacion_academica',
        'datos': formaciones,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now()
    })

def nacionalidad(request):
    """
    Noviembre 14, 2015
    Autor: Daniel Correa

    Permite conocer el numero de deportistas colombianos y extranjeros
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicDeportistaView
    else:
        tabla = TenantDeportistaView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        consultas = [
            "list("+tabla.__name__+".objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('nacionalidad__nombre')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('nacionalidad__nombre')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,genero__in=%s).annotate(descripcion=F('nacionalidad__nombre')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0).annotate(descripcion=F('nacionalidad__nombre')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
        ]

        nacionalidades = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)

        return JsonResponse(nacionalidades)

    else:
        nacionalidades = list(tabla.objects.filter(estado=0).annotate(descripcion=F('nacionalidad__nombre')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        nacionalidades = tipoTenant.ajustar_resultado(nacionalidades)

    visualizaciones = [1, 2, 3,5,6,7]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Nacionalidad de los deportistas',
        'url_data' : 'reporte_nacionalidad',
        'datos': nacionalidades,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now()
    })

def tipo_lesion(request):
    """
    Diciembre 18, 2015
    Autor: Daniel Correa

    Permite conocer la cantidad de deportistas organizados por tipo de lesion
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicDeportistaView
    else:
        tabla = TenantDeportistaView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        consultas = [
            "list("+tabla.__name__+".objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('tipo_lesion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('tipo_lesion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,genero__in=%s).annotate(descripcion=F('tipo_lesion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0).annotate(descripcion=F('tipo_lesion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
        ]

        lesiones = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)
        lesiones = tabla.return_display_tipo_lesion(tabla,lesiones)

        return JsonResponse(lesiones)

    else:
        lesiones = list(tabla.objects.filter(estado=0).annotate(descripcion=F('tipo_lesion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        lesiones = tipoTenant.ajustar_resultado(lesiones)
        lesiones = tabla.return_display_tipo_lesion(tabla,lesiones)


    visualizaciones = [1, 2, 3, 5]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Deportistas por tipos de lesion',
        'url_data' : 'reporte_tipo_lesion',
        'datos': lesiones,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now()
    })

def periodo_lesion(request):
    pass