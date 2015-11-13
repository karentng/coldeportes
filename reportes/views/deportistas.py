#encoding:utf-8
from django.shortcuts import render, redirect
from snd.models import HistorialDeportivo
from django.db.models import Count
from reportes.forms import FiltrosDeportistasForm
from django.db.models import F

def participaciones_deportivas(request):
    """
    Reporte participaciones deportivas:
    Consulta que trae el numero de  participaciones deportiva ordenadas por tipo
    """
    tipoTenant = request.tenant.obtenerTenant()
    if request.is_ajax():
        pass
    else:
        #Traer la cantidad de hisotriales ordenados por tipo
        centros = tipoTenant.ejecutar_consulta(True, "list(HistorialDeportivo.objects.annotate(descripcion=F('tipo')).values('descripcion').annotate(cantidad=Count('tipo')))")
        consulta = HistorialDeportivo.objects.annotate(descripcion=F('tipo')).values('descripcion').annotate(cantidad=Count('tipo'))
        print(consulta)

    visualizaciones = [1, 2, 3]
    form = FiltrosDeportistasForm(visualizaciones=visualizaciones)
    return render(request, 'deportistas/participaciones_deportivas.html', {
        'centros': centros,
        'visualizaciones': visualizaciones,
        'form': form,
    })
