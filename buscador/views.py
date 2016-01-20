#encoding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse

from buscador.forms import BuscadorCafForm
from entidades.modelos_vistas_reportes import PublicCafView
from coldeportes.utilities import get_request_or_none

def add_kwarg(kwargs, campo, valor):
    if valor:
        kwargs.update({campo: valor})
    return kwargs

def model_to_list(datos, campos):
    lista = []
    for i in datos:
        aux = []
        for campo in campos:
            aux.append(getattr(i, campo).__str__())
        lista.append(aux)
    return lista

def centros_acondicionamiento(request):
    form = BuscadorCafForm()
    
    if request.is_ajax():
        nombre = get_request_or_none(request.GET, 'nombre')
        ciudad = get_request_or_none(request.GET, 'ciudades')
        departamento = get_request_or_none(request.GET, 'departamentos')

        kwargs = {}
        kwargs = add_kwarg(kwargs, 'nombre__icontains', nombre)
        kwargs = add_kwarg(kwargs, 'ciudad__in', ciudad)
        kwargs = add_kwarg(kwargs, 'ciudad__departamento__in', departamento)
        
        if kwargs != {}:
            datos = PublicCafView.objects.filter(**kwargs)
        else:
            datos = PublicCafView.objects.all()
        datos = model_to_list(datos, ["nombre", "ciudad", "direccion", "telefono"])
        
        return JsonResponse({"data":datos})

    return render(request, 'centros_acondicionamiento.html', {
        'form': form,
    })