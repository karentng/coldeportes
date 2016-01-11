#encoding:utf-8
from django.shortcuts import render, redirect
from snd.modelos.deportistas import HistorialDeportivo,Deportista,InformacionAdicional,Deportista,InformacionAcademica
from entidades.models import Departamento
from django.db.models import Count
from reportes.formularios.deportistas import FiltrosDeportistasForm,FiltrosDeportistasCategoriaForm
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
        beneficiados = tipoTenant.ajustar_resultado(beneficiados)
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
            usa_centros['Usa centros biomédicos'] = usa_centros[True]
            del usa_centros[True]
        if False in usa_centros:
            usa_centros['No usa centros biomédicos'] = usa_centros[False]
            del usa_centros[False]


        return JsonResponse(usa_centros)

    else:
        usa_centros = list(tabla.objects.filter(estado = 0).annotate(descripcion=F('usa_centros_biomedicos')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        usa_centros = tipoTenant.ajustar_resultado(usa_centros)

        if True in usa_centros:
            usa_centros['Usa centros biomédicos'] = usa_centros[True]
            del usa_centros[True]
        if False in usa_centros:
            usa_centros['No usa centros biomédicos'] = usa_centros[False]
            del usa_centros[False]

    visualizaciones = [1, 2, 3, 5, 6, 7]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Uso de centros biomédicos',
        'url_data' : 'reporte_uso_centros_biomedicos',
        'datos': usa_centros,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now()
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
            lgtbi['Pertenece a la comunidad LGTBI'] = lgtbi[True]
            del lgtbi[True]
        if False in lgtbi:
            lgtbi['No pertenece a la comunidad LGTBI'] = lgtbi[False]
            del lgtbi[False]

        return JsonResponse(lgtbi)

    else:
        lgtbi = list(tabla.objects.filter(estado = 0).annotate(descripcion=F('lgtbi')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        lgtbi = tipoTenant.ajustar_resultado(lgtbi)

        if True in lgtbi:
            lgtbi['Pertenece a la comunidad LGTBI'] = lgtbi[True]
            del lgtbi[True]
        if False in lgtbi:
            lgtbi['No pertenece a la comunidad LGTBI'] = lgtbi[False]
            del lgtbi[False]

    visualizaciones = [1, 2, 3, 5, 6, 7]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Deportistas que pertenecen a la comunidad LGTBI',
        'url_data' : 'reporte_lgtbi_deportistas',
        'datos': lgtbi,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now()
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

        consultas = [
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('fecha_doping')).values('descripcion').annotate(cantidad=Count('fecha_doping',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('fecha_doping')).values('descripcion').annotate(cantidad=Count('fecha_doping',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0,genero__in=%s).annotate(descripcion=F('fecha_doping')).values('descripcion').annotate(cantidad=Count('fecha_doping',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado = 0).annotate(descripcion=F('fecha_doping')).values('descripcion').annotate(cantidad=Count('fecha_doping',distinct=True)))",
        ]

        beneficiados = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)
        beneficiados = tipoTenant.ajustar_resultado(beneficiados)
        if True in beneficiados:
            beneficiados['Deportistas con reportes de doping'] = beneficiados[True]
            del beneficiados[True]
        if False in beneficiados:
            beneficiados['Deportistas sin reportes de doping'] = beneficiados[False]
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
        print(tabla.objects.filter(estado = 0).order_by('id').distinct('id'))
        total_deportistas = len(tabla.objects.filter(estado = 0).order_by('id').distinct('id'))
        print(total_deportistas)

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
        formaciones = tipoTenant.ajustar_resultado(formaciones)

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
        nacionalidades = tipoTenant.ajustar_resultado(nacionalidades)

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
        tipo = True if reporte == 'TL' else False

        consultas = [
            "list("+tabla.__name__+".objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s,genero__in=%s).annotate(descripcion=F('"+categoria+"')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,ciudad_residencia__departamento__id__in=%s).annotate(descripcion=F('"+categoria+"')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0,genero__in=%s).annotate(descripcion=F('"+categoria+"')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
            "list("+tabla.__name__+".objects.filter(estado=0).annotate(descripcion=F('"+categoria+"')).values('descripcion').annotate(cantidad=Count('id',distinct=True)))",
        ]

        lesiones = ejecutar_casos_recursivos(consultas,departamentos,genero,tipoTenant)
        lesiones = tipoTenant.ajustar_resultado(lesiones)
        lesiones = tabla.return_display_lesion(tabla,lesiones,tipo)

        return JsonResponse(lesiones)

    else:
        lesiones = list(tabla.objects.filter(estado=0).annotate(descripcion=F(categoria)).values('descripcion').annotate(cantidad=Count('id',distinct=True)))
        lesiones = tipoTenant.ajustar_resultado(lesiones)
        lesiones = tabla.return_display_lesion(tabla,lesiones,True)

    visualizaciones = [1, 2, 3, 5]
    form = FiltrosDeportistasCategoriaForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/base_deportistas.html', {
        'nombre_reporte' : 'Tipo de lesión',
        'url_data' : 'reporte_lesiones',
        'datos': lesiones,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Deportistas',
        'fecha_generado': datetime.now(),
        'agrupado': True
    })