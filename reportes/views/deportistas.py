#encoding:utf-8
from django.shortcuts import render, redirect
from snd.modelos.deportistas import HistorialLesiones
from entidades.models import Departamento,Nacionalidad
from django.db.models import Count
from reportes.formularios.deportistas import FiltrosDeportistasForm,FiltrosDeportistasCategoriaForm
from django.db.models import F
import ast
from datetime import datetime
from django.http import JsonResponse
from entidades.modelos_vistas_reportes import PublicDeportistaView
from reportes.models import TenantDeportistaView
from reportes.utilities import sumar_datos_diccionario,fecha_nacimiento_maxima

def ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant):
    """
    Noviembre 13, 2015
    Autor: Daniel Correa

    Permite ejecutar los diferentes filtros de casos de acuerdo a un arreglo de consultas
    CONSULTAS LLEVA EL SIGUIENTE FORMATO [contulta caso 1, consulta caso 2 , consulta caso 3, ... ,consulta caso n]
    LOS CASOS EMPIEZAN EN 1 EL DE MAS ARRIBA HASTA N EL DE MAS ABAJO
    """
    if departamentos and genero:
        resultado = eval(consultas[0]%(departamentos,genero))
    elif departamentos:
        resultado = eval(consultas[1]%(departamentos))
    elif genero:
        resultado = eval(consultas[2]%(genero))
    else:
        resultado = eval(consultas[3])
    return resultado

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
        participaciones = tipoTenant.ajustar_resultado(participaciones)

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
        'fecha_generado': datetime.now(),
        'nombres_columnas':['Descripción']
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
        beneficiados = tipoTenant.ajustar_resultado(beneficiados)

        if True in beneficiados:
            beneficiados['DEPORTISTAS BENEFICIADOS'] = beneficiados[True]
            del beneficiados[True]
        if None in beneficiados or False in beneficiados:
            try:
                beneficiados['DEPORTISTAS NO BENEFICIADOS'] = beneficiados[None]
                del beneficiados[None]
            except Exception:
                beneficiados['DEPORTISTAS NO BENEFICIADOS'] = beneficiados[False]
                del beneficiados[False]

        return JsonResponse(beneficiados)

    else:
        beneficiados = list(tabla.objects.filter(estado = 0).annotate(descripcion=F('es_beneficiario_programa_apoyo')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        beneficiados = tipoTenant.ajustar_resultado(beneficiados)

        if True in beneficiados:
            beneficiados['DEPORTISTAS BENEFICIADOS'] = beneficiados[True]
            del beneficiados[True]
        if None in beneficiados or False in beneficiados:
            try:
                beneficiados['DEPORTISTAS NO BENEFICIADOS'] = beneficiados[None]
                del beneficiados[None]
            except Exception:
                beneficiados['DEPORTISTAS NO BENEFICIADOS'] = beneficiados[False]
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
        'fecha_generado': datetime.now(),
        'nombres_columnas':["Descripción"]
    })


def reporte_uso_centros_biomedicos(request):
    """
    Diciembre 21, 2015
    Autor: Milton Lenis

    Permite conocer el numero de deportistas que usan centros biomédicos
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
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('usa_centros_biomedicos')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('usa_centros_biomedicos')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,genero__in=%s).annotate(descripcion=F('usa_centros_biomedicos')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0).annotate(descripcion=F('usa_centros_biomedicos')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
        ]

        usa_centros = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)
        usa_centros = tipoTenant.ajustar_resultado(usa_centros)

        if True in usa_centros:
            usa_centros['USAN CENTROS BIOMÉDICOS'] = usa_centros[True]
            del usa_centros[True]
        if None in usa_centros or False in usa_centros:
            try:
                usa_centros['NO USAN CENTROS BIOMÉDICOS'] = usa_centros[None]
                del usa_centros[None]
            except Exception:
                usa_centros['NO USAN CENTROS BIOMÉDICOS'] = usa_centros[False]
                del usa_centros[False]

        return JsonResponse(usa_centros)

    else:
        usa_centros = list(tabla.objects.filter(estado = 0).annotate(descripcion=F('usa_centros_biomedicos')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        usa_centros = tipoTenant.ajustar_resultado(usa_centros)
        if True in usa_centros:
            usa_centros['USAN CENTROS BIOMÉDICOS'] = usa_centros[True]
            del usa_centros[True]
        if None in usa_centros or False in usa_centros:
            try:
                usa_centros['NO USAN CENTROS BIOMÉDICOS'] = usa_centros[None]
                del usa_centros[None]
            except Exception:
                usa_centros['NO USAN CENTROS BIOMÉDICOS'] = usa_centros[False]
                del usa_centros[False]


    visualizaciones = [1, 2, 3, 5, 6]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Cantidad de deportistas que usan centros biomédicos',
        'url_data' : 'reporte_uso_centros_biomedicos',
        'datos': usa_centros,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now(),
        'nombres_columnas':["Descripción"]
    })


def reporte_lgtbi(request):
    """
    Diciembre 21, 2015
    Autor: Milton Lenis

    Permite conocer el numero de deportistas que pertenecen a la comunidad LGTBI
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
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,genero__in=%s).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
        ]

        lgtbi = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)
        lgtbi = tipoTenant.ajustar_resultado(lgtbi)

        if True in lgtbi:
            lgtbi['PERTENECE A LA COMUNIDAD LGTBI'] = lgtbi[True]
            del lgtbi[True]
        if False in lgtbi or None in lgtbi:
            try:
                lgtbi['NO PERTENECE A LA COMUNIDAD LGTBI'] = lgtbi[False]
                del lgtbi[False]
            except Exception:
                lgtbi['NO PERTENECE A LA COMUNIDAD LGTBI'] = lgtbi[None]
                del lgtbi[None]

        return JsonResponse(lgtbi)

    else:
        lgtbi = list(tabla.objects.filter(estado = 0).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        lgtbi = tipoTenant.ajustar_resultado(lgtbi)
        if True in lgtbi:
            lgtbi['PERTENECE A LA COMUNIDAD LGTBI'] = lgtbi[True]
            del lgtbi[True]
        if False in lgtbi or None in lgtbi:
            try:
                lgtbi['NO PERTENECE A LA COMUNIDAD LGTBI'] = lgtbi[False]
                del lgtbi[False]
            except Exception:
                lgtbi['NO PERTENECE A LA COMUNIDAD LGTBI'] = lgtbi[None]
                del lgtbi[None]

    visualizaciones = [1, 2, 3, 5, 6]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Cantidad de deportistas que pertenecen a la comunidad LGTBI',
        'url_data' : 'reporte_lgtbi_deportistas',
        'datos': lgtbi,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now(),
        'nombres_columnas':["Descripción"]
    })


def reporte_doping(request):
    """
    Diciembre 21, 2015
    Autor: Milton Lenis

    Permite conocer el numero de deportistas con algún reporte de doping
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicDeportistaView
    else:
        tabla = TenantDeportistaView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        consultas_con_doping = [
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s,genero__in=%s).exclude(fecha_doping=None).order_by('id').distinct('id'))",
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s).exclude(fecha_doping=None).order_by('id').distinct('id'))",
            "list("+tabla.__name__+".objects.filter(estado = 0,genero__in=%s).exclude(fecha_doping=None).order_by('id').distinct('id'))",
            "list("+tabla.__name__+".objects.filter(estado = 0).exclude(fecha_doping=None).order_by('id').distinct('id'))",
        ]

        consultas_sin_doping = [
            "list("+tabla.__name__+".objects.filter(estado = 0,fecha_doping=None,ciudad_residencia__departamento__id__in=%s,genero__in=%s).order_by('id').distinct('id'))",
            "list("+tabla.__name__+".objects.filter(estado = 0,fecha_doping=None,ciudad_residencia__departamento__id__in=%s).order_by('id').distinct('id'))",
            "list("+tabla.__name__+".objects.filter(estado = 0,fecha_doping=None,genero__in=%s).order_by('id').distinct('id'))",
            "list("+tabla.__name__+".objects.filter(estado = 0, fecha_doping=None).order_by('id').distinct('id'))",
        ]

        doping = {}
        doping['DEPORTISTAS CON REPORTES DE DOPING'] = len(ejecutar_casos_recursivos(consultas_con_doping,departamentos,genero,tipoTenant))
        doping['DEPORTISTAS SIN REPORTES DE DOPING'] = len(ejecutar_casos_recursivos(consultas_sin_doping,departamentos,genero,tipoTenant))

        return JsonResponse(doping)

    else:
        doping = {}
        doping['DEPORTISTAS CON REPORTES DE DOPING'] = len(tabla.objects.filter(estado = 0).exclude(fecha_doping=None).order_by('id').distinct('id'))
        doping['DEPORTISTAS SIN REPORTES DE DOPING'] = len(tabla.objects.filter(estado = 0, fecha_doping=None).order_by('id').distinct('id'))

    visualizaciones = [1, 2, 3, 5, 6]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Cantidad de deportistas con reportes de doping',
        'url_data' : 'reporte_doping',
        'datos': doping,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now(),
        'nombres_columnas':["Descripción"]
    })


def reporte_cantidad_total_deportistas(request):
    """
    Diciembre 21, 2015
    Autor: Milton Lenis

    Permite conocer el número total de deportistas
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicDeportistaView
    else:
        tabla = TenantDeportistaView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null' else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        consultas = [
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s,genero__in=%s).order_by('id').distinct('id'))",
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s).order_by('id').distinct('id'))",
            "list("+tabla.__name__+".objects.filter(estado = 0,genero__in=%s).order_by('id').distinct('id'))",
            "list("+tabla.__name__+".objects.filter(estado = 0).order_by('id').distinct('id'))",
        ]

        total_deportistas = len(ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant))

        resultado = {
            'Total Deportistas':total_deportistas
        }

        return JsonResponse(resultado)

    else:
        total_deportistas = len(tabla.objects.filter(estado = 0).order_by('id').distinct('id'))

        resultado = {
            'Total Deportistas':total_deportistas
        }

    visualizaciones = [1, 2, 3, 5, 6, 7]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Cantidad TOTAL de deportistas',
        'url_data' : 'reporte_cantidad_total_deportistas',
        'datos': resultado,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now(),
        'nombres_columnas':["Descripción"]
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
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Etnias de los deportistas',
        'url_data' : 'reporte_etinias_deportistas',
        'datos': etnias,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now(),
        'nombres_columnas':["Etnia"]
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
        formaciones = tipoTenant.ajustar_resultado(formaciones)

        return JsonResponse(formaciones)

    else:
        formaciones = list(tabla.objects.filter(estado=0,estado_formacion='Finalizado').annotate(descripcion=F('nivel_formacion')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        formaciones = tipoTenant.ajustar_resultado(formaciones)

    visualizaciones = [1, 2, 3, 5, 6, 7]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Formación académica de los deportistas',
        'url_data' : 'reporte_formacion_academica',
        'datos': formaciones,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now(),
        'nombres_columnas':["Nivel Académico"]
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
        nacionalidades = tipoTenant.ajustar_resultado(nacionalidades)

        return JsonResponse(nacionalidades)

    else:
        nacionalidades = list(tabla.objects.filter(estado=0).annotate(descripcion=F('nacionalidad__nombre')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        nacionalidades = tipoTenant.ajustar_resultado(nacionalidades)

    return nacionalidades

def extranjeros(request):
    """
    Enero 16, 2016
    Autor: Daniel Correa

    Esta vista implementa el reporte de cantidad de extranjeros y colombianos
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicDeportistaView
    else:
        tabla = TenantDeportistaView

    colombia = Nacionalidad.objects.filter(iso='CO')

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])

        consultas = [
            tabla.__name__+".objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,genero__in=%s)",
            tabla.__name__+".objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s)",
            tabla.__name__+".objects.filter(estado=0,genero__in=%s)",
            tabla.__name__+".objects.filter(estado=0)",
        ]

        consulta_general = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)
        consulta_completa = list(consulta_general.filter(nacionalidad=colombia).annotate(descripcion=F('nacionalidad__nombre')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        numero_extranjeros = consulta_general.exclude(nacionalidad=colombia).count()
        consulta_completa.append({'cantidad':numero_extranjeros,'descripcion':'Extranjeros'})
        consulta_completa = tipoTenant.ajustar_resultado(consulta_completa)

        return JsonResponse(consulta_completa)

    else:
        consulta_general = tabla.objects.filter(estado=0)
        consulta_completa = list(consulta_general.filter(nacionalidad=colombia).annotate(descripcion=F('nacionalidad__nombre')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        numero_extranjeros = consulta_general.exclude(nacionalidad=colombia).count()
        consulta_completa.append({'cantidad':numero_extranjeros,'descripcion':'Extranjeros'})
        consulta_completa = tipoTenant.ajustar_resultado(consulta_completa)


    return consulta_completa

def extranjeros_vs_nacionalidad(request):
    """
    Enero 21, 2016
    Autor: Daniel Correa

    Esta vista implementa el reporte de cantidad de extranjeros y colombianos vs nacionalidad de los deportistas
    """

    reporte = 'NA'

    if request.is_ajax():

        reporte = 'NA' if request.GET['reporte'] == 'null'  else ast.literal_eval(request.GET['reporte'])

        return nacionalidad(request) if reporte == 'NA' else extranjeros(request)
    else:
        print('antes')
        datos = nacionalidad(request) if reporte == 'NA' else extranjeros(request)
        print('dsps')

    visualizaciones = [1, 2, 3,5,6,7]
    TIPO_REPORTE = (
        ('NA', 'Número de deportistas por Nacionalidad'),
        ('EX', 'Número de deportistas Colombianos vs Extranjeros'),
    )
    form = FiltrosDeportistasCategoriaForm(visualizaciones=visualizaciones,TIPO_REPORTE=TIPO_REPORTE)

    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Número de deportistas por nacionalidad',
        'nombre_generador': 'Deportistas extranjeros vs deportistas por nacionalidad',
        'url_data' : 'reporte_nacional_extranjero',
        'datos': datos,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now(),
        'agrupado': True,
        'nombres_columnas':["Descripción"]
    })


def lesiones_deportivas(request):
    """
    Diciembre 22, 2015
    Autor: Daniel Correa

    Esta vista reune la implementación de los reportes de lesiones deportivas caractetirzadas por tipo de lesion
    y perido de rehabilitación
    """
    tipoTenant = request.tenant.obtenerTenant()

    if tipoTenant.schema_name == 'public':
        tabla = PublicDeportistaView
    else:
        tabla = TenantDeportistaView

    categoria = 'tipo_lesion'

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        genero = None if request.GET['genero'] == 'null'  else ast.literal_eval(request.GET['genero'])
        reporte = None if request.GET['reporte'] == 'null'  else ast.literal_eval(request.GET['reporte'])
        categoria = 'tipo_lesion' if reporte == 'TL' else 'periodo_rehabilitacion'
        tipo = HistorialLesiones.TIPOS_LESION if reporte == 'TL' else HistorialLesiones.PERIODOS_REHABILITACION

        consultas = [
            "list("+tabla.__name__+".objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('"+categoria+"')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('"+categoria+"')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,genero__in=%s).annotate(descripcion=F('"+categoria+"')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0).annotate(descripcion=F('"+categoria+"')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
        ]

        lesiones = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)
        lesiones = sumar_datos_diccionario(lesiones,tipo)

        return JsonResponse(lesiones)

    else:
        lesiones = list(tabla.objects.filter(estado=0).annotate(descripcion=F(categoria)).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        lesiones = sumar_datos_diccionario(lesiones,HistorialLesiones.TIPOS_LESION)
    visualizaciones = [1, 2, 3, 5]
    TIPO_REPORTE = (
        ('TL', 'Tipo de lesión'),
        ('PL', 'Periodo de lesión'),
    )
    form = FiltrosDeportistasCategoriaForm(visualizaciones=visualizaciones,TIPO_REPORTE=TIPO_REPORTE)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte': 'Tipo de lesión',
        'nombre_generador': 'Lesiones de los deportistas',
        'url_data': 'reporte_lesiones',
        'datos': lesiones,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now(),
        'agrupado': True,
        'nombres_columnas':["Tipo de lesión","Periodo de rehabilitación"]
    })

def ordenar_edades_rangos(deportistas):
    edades = []
    fechas_maximas = fecha_nacimiento_maxima([13,18,25,50])
    uno_doce = {'descripcion':'Niños (1-12 años)','cantidad':deportistas.filter(fecha_nacimiento__lte=fechas_maximas[0]).count()}
    edades.append(uno_doce)
    trece_diezsiete = {'descripcion':'Jovenes (13-17 años)','cantidad':deportistas.filter(fecha_nacimiento__gte=fechas_maximas[0],fecha_nacimiento__lte=fechas_maximas[1]).count()}
    edades.append(trece_diezsiete)
    diezocho_veinticinco = {'descripcion':'Adultos Jovenes (18-25 años)','cantidad':deportistas.filter(fecha_nacimiento__gte=fechas_maximas[1],fecha_nacimiento__lte=fechas_maximas[2]).count()}
    edades.append(diezocho_veinticinco)
    veinticinco_cincuenta = {'descripcion':'Adultos (25-50 años)','cantidad':deportistas.filter(fecha_nacimiento__gte=fechas_maximas[2],fecha_nacimiento__lte=fechas_maximas[3]).count()}
    edades.append(veinticinco_cincuenta)
    cincuenta_mas = {'descripcion':'Adultos Mayores (> 50 años)','cantidad':deportistas.filter(fecha_nacimiento__gte=fechas_maximas[3]).count()}
    edades.append(cincuenta_mas)
    return edades

def edad_deportistas(request):
    """
    Enero 24, 2016
    Autor: Daniel Correa

    Permite ver la cantidad de deportistas ordenados por rangos de edad

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
            tabla.__name__+".objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,genero__in=%s)",
            tabla.__name__+".objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s)",
            tabla.__name__+".objects.filter(estado=0,genero__in=%s)",
            tabla.__name__+".objects.filter(estado=0)",
        ]

        deportistas = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)
        edades = ordenar_edades_rangos(deportistas)
        edades = tipoTenant.ajustar_resultado(edades)

        return JsonResponse(edades)

    else:
        deportistas = tabla.objects.filter(estado=0)
        edades = ordenar_edades_rangos(deportistas)
        edades = tipoTenant.ajustar_resultado(edades)

    visualizaciones = [1, 2, 3, 5]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte': 'Edades de los deportistas',
        'url_data': 'reporte_edad_deportistas',
        'datos': edades,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now(),
        'nombres_columnas':["Rangos de Edades"]
    })