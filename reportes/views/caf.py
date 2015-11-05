#encoding:utf-8
from django.shortcuts import render, redirect
from snd.models import CentroAcondicionamiento
from django.db.models import Count, F
from reportes.forms import DemografiaForm
from django.db import models
'''
Reportes:
    1. Dona
    2. Comparativa Horizontal
    3. Comparativa Vertical
    4. Tree Map
'''

def demografia(request):
    tipoTenant = request.tenant.obtenerTenant()
    #ubicaciones = tipoTenant.atributos_cafs()

    #print (ubicaciones)

    def hola(model, args):
        print (args)

    hola(CentroAcondicionamiento,
        (
            ("annotate", "descripcion=F('ciudad__departamento__nombre')"),
            ("values", "descripcion"),
            ("annotate", "cantidad=Count('ciudad__departamento')")
        )
    )

    
    centros = list(CentroAcondicionamiento.objects.annotate(descripcion=F('ciudad__departamento__nombre')).values("descripcion").annotate(cantidad=Count('ciudad__departamento')))
    visualizaciones = [1, 3]
    print ("============")
    print ("============")
    print (centros)
    form = DemografiaForm()
    return render(request, 'caf/demografia.html', {
        'centros': centros,
        'visualizaciones': visualizaciones,
        'form': form,
    })