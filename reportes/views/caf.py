#encoding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import F, Count

import ast
from datetime import date

from reportes.forms import DemografiaForm
from entidades.modelos_vistas_reportes import PublicCafView
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
                    centros += tabla.objects.filter(ciudad__departamento__id__in=departamentos, fecha_creacion__gte=date(anno, 1, 1), fecha_creacion__lte=date(anno, 12, 31)).annotate(descripcion=F('ciudad__nombre')).values('descripcion').annotate(cantidad=Count('ciudad'))
            else:
                centros = list(tabla.objects.filter(ciudad__departamento__id__in=departamentos).annotate(descripcion=F('ciudad__nombre')).values('descripcion').annotate(cantidad=Count('ciudad')))
        else:
            if annos:
                centros = list()
                for anno in annos:
                    anno = int(anno)
                    centros += tabla.objects.filter(fecha_creacion__gte=date(anno, 1, 1), fecha_creacion__lte=date(anno, 12, 31)).annotate(descripcion=F('ciudad__departamento__nombre')).values('descripcion').annotate(cantidad=Count('ciudad__departamento'))
            else:
                centros = list(tabla.objects.annotate(descripcion=F('ciudad__departamento__nombre')).values('descripcion').annotate(cantidad=Count('ciudad__departamento')))
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
        centros = list(tabla.objects.annotate(descripcion=F('ciudad__departamento__nombre')).values('descripcion').annotate(cantidad=Count('ciudad__departamento')))
        centros = tipoTenant.ajustar_resultado(centros)
    visualizaciones = [1, 2, 3]

    form = DemografiaForm(visualizaciones=visualizaciones)
    return render(request, 'caf/demografia.html', {
        'centros': centros,
        'visualizaciones': visualizaciones,
        'form': form,

    })
