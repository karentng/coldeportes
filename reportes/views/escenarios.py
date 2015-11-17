#encoding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
import ast
from reportes.formularios.escenarios import EstratoForm

'''
Reportes:
    1. Dona
    2. Comparativa Horizontal
    3. Comparativa Vertical
    4. Tree Map
'''

def estrato(request):
    tipoTenant = request.tenant.obtenerTenant()

    if request.is_ajax():
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        annos = None if request.GET['annos'] == 'null'  else ast.literal_eval(request.GET['annos'])
        disciplina = None if request.GET['disciplina'] == 'null' else ast.literal_eval(request.GET['disciplina'])
        
        return JsonResponse({})
    else:
        escenarios = tipoTenant.ejecutar_consulta(False, "list(Escenario.objects.annotate(descripcion_=F('estrato')).values('descripcion_').annotate(cantidad=Count('estrato')))")
    visualizaciones = [1, 2, 3]

    form = EstratoForm(visualizaciones=visualizaciones)
    return render(request, 'escenarios/estrato.html', {
        'escenarios': escenarios,
        'visualizaciones': visualizaciones,
        'form': form,
    })