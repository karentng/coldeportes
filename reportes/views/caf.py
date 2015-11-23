#encoding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import F, Count

import ast
from datetime import date

from entidades.modelos_vistas_reportes import PublicCafView
from reportes.formularios.caf import DemografiaForm
from reportes.models import TenantCafView
from snd.models import CentroAcondicionamiento

'''
Reportes:
    1. Dona
    2. Comparativa Horizontal
    3. Comparativa Vertical
    4. Tree Map
    5. Gráfico de cilindros
'''

def demografia(request):
    def casos_de_consulta(departamentos, annos, tabla, tipoTenant):
        if departamentos:
            if annos:
                centros = list()
                for anno in annos:
                    anno = int(anno)
                    centros += tabla.objects.filter(ciudad__departamento__id__in=departamentos, fecha_creacion__gte=date(anno, 1, 1), fecha_creacion__lte=date(anno, 12, 31)).annotate(descripcion=F('ciudad__nombre')).values('id', 'descripcion').annotate(cantidad=Count('ciudad', distinct=True))
            else:
                centros = list(tabla.objects.filter(ciudad__departamento__id__in=departamentos).annotate(descripcion=F('ciudad__nombre')).values('id', 'descripcion').annotate(cantidad=Count('ciudad', distinct=True)))
        else:
            if annos:
                centros = list()
                for anno in annos:
                    anno = int(anno)
                    centros += tabla.objects.filter(fecha_creacion__gte=date(anno, 1, 1), fecha_creacion__lte=date(anno, 12, 31)).annotate(descripcion=F('ciudad__departamento__nombre')).values('id', 'descripcion').annotate(cantidad=Count('ciudad__departamento', distinct=True))
            else:
                centros = list(tabla.objects.annotate(descripcion=F('ciudad__departamento__nombre')).values('id', 'descripcion').annotate(cantidad=Count('ciudad__departamento', distinct=True)))
        centros = tipoTenant.ajustar_resultado(centros)
        return centros

    tipoTenant = request.tenant.obtenerTenant()
    
    if tipoTenant.schema_name == 'public':
        tabla = PublicCafView
    else:
        tabla = TenantCafView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        annos = None if request.GET['annos'] == 'null'  else ast.literal_eval(request.GET['annos'])
        
        centros = casos_de_consulta(departamentos, annos, tabla, tipoTenant)

        return JsonResponse(centros)
    else:
        centros = list(tabla.objects.annotate(descripcion=F('ciudad__departamento__nombre')).values('id', 'descripcion').annotate(cantidad=Count('ciudad__departamento', distinct=True)))
        centros = tipoTenant.ajustar_resultado(centros)
    visualizaciones = [1, 2, 3]

    form = DemografiaForm(visualizaciones=visualizaciones)

    return render(request, 'caf/caf_template.html', {
        'nombre_reporte' : 'Centros de Acondicionamiento Físico por Departamentos y Municipios',
        'url_data' : 'reportes_caf_demografia',
        'datos': centros,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Centro de Acondicionamiento',
    })

def estratos(request):
    def casos_de_consulta(departamentos, annos, tabla, tipoTenant):
        if departamentos:
            if annos:
                centros = list()
                for anno in annos:
                    anno = int(anno)
                    centros += tabla.objects.filter(ciudad__departamento__id__in=departamentos, fecha_creacion__gte=date(anno, 1, 1), fecha_creacion__lte=date(anno, 12, 31)).values('id', 'estrato').annotate(cantidad=Count('estrato', distinct=True))
            else:
                centros = list(tabla.objects.filter(ciudad__departamento__id__in=departamentos).values('id', 'estrato').annotate(cantidad=Count('estrato', distinct=True)))
        else:
            if annos:
                centros = list()
                for anno in annos:
                    anno = int(anno)
                    centros += tabla.objects.filter(fecha_creacion__gte=date(anno, 1, 1), fecha_creacion__lte=date(anno, 12, 31)).values('id', 'estrato').annotate(cantidad=Count('estrato', distinct=True))
            else:
                centros = list(tabla.objects.values('id', 'estrato').annotate(cantidad=Count('estrato', distinct=True)))
        centros = tipoTenant.ajustar_resultado(centros, 'estrato')
        return centros

    tipoTenant = request.tenant.obtenerTenant()
    
    if tipoTenant.schema_name == 'public':
        tabla = PublicCafView
    else:
        tabla = TenantCafView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        annos = None if request.GET['annos'] == 'null'  else ast.literal_eval(request.GET['annos'])
        
        centros = casos_de_consulta(departamentos, annos, tabla, tipoTenant)

        return JsonResponse(centros)
    else:
        centros = list(tabla.objects.values('id', 'estrato').annotate(cantidad=Count('estrato', distinct=True)))
        centros = tipoTenant.ajustar_resultado(centros, 'estrato')
    visualizaciones = [1, 2, 3]

    form = DemografiaForm(visualizaciones=visualizaciones)

    return render(request, 'caf/caf_template.html', {
        'nombre_reporte' : 'Centros de Acondicionamiento Físico por Estratos',
        'url_data' : 'reportes_caf_estratos',
        'datos': centros,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Centro de Acondicionamiento',
    })


def clases(request):
    def casos_de_consulta(departamentos, annos, tabla, tipoTenant):
        if departamentos:
            if annos:
                centros = list()
                for anno in annos:
                    anno = int(anno)
                    centros += tabla.objects.exclude(nombre_clase=None).filter(ciudad__departamento__id__in=departamentos, fecha_creacion__gte=date(anno, 1, 1), fecha_creacion__lte=date(anno, 12, 31)).values('id', 'nombre_clase').annotate(cantidad=Count('nombre_clase', distinct=True))
            else:
                centros = list(tabla.objects.exclude(nombre_clase=None).filter(ciudad__departamento__id__in=departamentos).values('id', 'nombre_clase').annotate(cantidad=Count('nombre_clase', distinct=True)))
        else:
            if annos:
                centros = list()
                for anno in annos:
                    anno = int(anno)
                    centros += tabla.objects.exclude(nombre_clase=None).filter(fecha_creacion__gte=date(anno, 1, 1), fecha_creacion__lte=date(anno, 12, 31)).values('id', 'nombre_clase').annotate(cantidad=Count('nombre_clase', distinct=True))
            else:
                centros = list(tabla.objects.exclude(nombre_clase=None).values('id', 'nombre_clase').annotate(cantidad=Count('nombre_clase', distinct=True)))
        centros = tipoTenant.ajustar_resultado(centros, 'nombre_clase')
        return centros

    tipoTenant = request.tenant.obtenerTenant()
    
    if tipoTenant.schema_name == 'public':
        tabla = PublicCafView
    else:
        tabla = TenantCafView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        annos = None if request.GET['annos'] == 'null'  else ast.literal_eval(request.GET['annos'])
        
        centros = casos_de_consulta(departamentos, annos, tabla, tipoTenant)

        return JsonResponse(centros)
    else:
        centros = list(tabla.objects.exclude(nombre_clase=None).values('id', 'nombre_clase').annotate(cantidad=Count('nombre_clase', distinct=True)))
        centros = tipoTenant.ajustar_resultado(centros, 'nombre_clase')
    visualizaciones = [1, 2, 3]

    form = DemografiaForm(visualizaciones=visualizaciones)

    return render(request, 'caf/caf_template.html', {
        'nombre_reporte' : 'Centros de Acondicionamiento Físico que ofrecen ciertas Clases',
        'url_data' : 'reportes_caf_clases',
        'datos': centros,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Centro de Acondicionamiento',
    })

def tipos_servicios(request):
    def casos_de_consulta(departamentos, annos, tabla, tipoTenant):
        if departamentos:
            if annos:
                centros = list()
                for anno in annos:
                    anno = int(anno)
                    centros += tabla.objects.exclude(nombre_servicio=None).filter(ciudad__departamento__id__in=departamentos, fecha_creacion__gte=date(anno, 1, 1), fecha_creacion__lte=date(anno, 12, 31)).values('id', 'nombre_servicio').annotate(cantidad=Count('nombre_servicio', distinct=True))
            else:
                centros = list(tabla.objects.exclude(nombre_servicio=None).filter(ciudad__departamento__id__in=departamentos).values('id', 'nombre_servicio').annotate(cantidad=Count('nombre_servicio', distinct=True)))
        else:
            if annos:
                centros = list()
                for anno in annos:
                    anno = int(anno)
                    centros += tabla.objects.exclude(nombre_servicio=None).filter(fecha_creacion__gte=date(anno, 1, 1), fecha_creacion__lte=date(anno, 12, 31)).values('id', 'nombre_servicio').annotate(cantidad=Count('nombre_servicio', distinct=True))
            else:
                centros = list(tabla.objects.exclude(nombre_servicio=None).values('id', 'nombre_servicio').annotate(cantidad=Count('nombre_servicio', distinct=True)))
        centros = tipoTenant.ajustar_resultado(centros, 'nombre_servicio')
        return centros

    tipoTenant = request.tenant.obtenerTenant()
    
    if tipoTenant.schema_name == 'public':
        tabla = PublicCafView
    else:
        tabla = TenantCafView

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        annos = None if request.GET['annos'] == 'null'  else ast.literal_eval(request.GET['annos'])
        
        centros = casos_de_consulta(departamentos, annos, tabla, tipoTenant)

        return JsonResponse(centros)
    else:
        centros = list(tabla.objects.exclude(nombre_servicio=None).values('id', 'nombre_servicio').annotate(cantidad=Count('nombre_servicio', distinct=True)))
        centros = tipoTenant.ajustar_resultado(centros, 'nombre_servicio')
    visualizaciones = [1, 2, 3]

    form = DemografiaForm(visualizaciones=visualizaciones)

    return render(request, 'caf/caf_template.html', {
        'nombre_reporte' : 'Centros de Acondicionamiento Físico que ofrecen ciertos Servicios',
        'url_data' : 'reportes_caf_tipos_servicios',
        'datos': centros,
        'visualizaciones': visualizaciones,
        'form': form,
        'actor': 'Centro de Acondicionamiento',
    })