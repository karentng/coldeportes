#encoding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
import ast
from reportes.forms import DemografiaForm

'''
Reportes:
    1. Dona
    2. Comparativa Horizontal
    3. Comparativa Vertical
    4. Tree Map
    5. Gráfico de cilindros
'''

def demografia(request):
    tipoTenant = request.tenant.obtenerTenant()

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        annos = None if request.GET['annos'] == 'null'  else ast.literal_eval(request.GET['annos'])
        
        if departamentos:
            if annos:
                centros = list()
                for anno in annos:
                    centros += tipoTenant.ejecutar_consulta(False, "list(CentroAcondicionamiento.objects.filter(ciudad__departamento__id__in=%s, fecha_creacion__gte=date(%s, 1, 1), fecha_creacion__lte=date(%s, 12, 31)).annotate(descripcion=F('ciudad__nombre')).values('descripcion').annotate(cantidad=Count('ciudad')))"%(departamentos, anno, anno))
                centros = tipoTenant.ajustar_resultado(centros)
            else:
                centros = tipoTenant.ejecutar_consulta(True, "list(CentroAcondicionamiento.objects.filter(ciudad__departamento__id__in=%s).annotate(descripcion=F('ciudad__nombre')).values('descripcion').annotate(cantidad=Count('ciudad')))"%(departamentos))
        else:
            if annos:
                centros = list()
                for anno in annos:
                    centros += tipoTenant.ejecutar_consulta(False, "list(CentroAcondicionamiento.objects.filter(fecha_creacion__gte=date(%s, 1, 1), fecha_creacion__lte=date(%s, 12, 31)).annotate(descripcion=F('ciudad__departamento__nombre')).values('descripcion').annotate(cantidad=Count('ciudad__departamento')))"%(anno, anno))
                    print (centros)
                centros = tipoTenant.ajustar_resultado(centros)
            else:
                centros = tipoTenant.ejecutar_consulta(True, "list(CentroAcondicionamiento.objects.annotate(descripcion=F('ciudad__departamento__nombre')).values('descripcion').annotate(cantidad=Count('ciudad__departamento')))")
        return JsonResponse(centros)
    else:
        centros = tipoTenant.ejecutar_consulta(True, "list(CentroAcondicionamiento.objects.annotate(descripcion=F('ciudad__departamento__nombre')).values('descripcion').annotate(cantidad=Count('ciudad__departamento')))")
    
    visualizaciones = [1, 2, 3]

    form = DemografiaForm(visualizaciones=visualizaciones)
    return render(request, 'caf/demografia.html', {
        'centros': centros,
        'visualizaciones': visualizaciones,
        'form': form,
    })