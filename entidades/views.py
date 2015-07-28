import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from entidades.models import *
from entidades.forms import *
from django.conf import settings
from django.contrib import messages

@login_required
def tipo(request):
    return render(request, 'entidad_tipo.html', {
    })

@login_required
def registro(request, tipo):
    form = EntidadForm()
    form2 = ActoresForm()

    dominio = settings.SUBDOMINIO_URL

    if request.method == 'POST':
        form = EntidadForm(request.POST)
        form2 = ActoresForm(request.POST)
        if form.is_valid() and form2.is_valid():
            actores = form2.save()

            pagina = form.cleaned_data['pagina']
            obj = form.save(commit=False)
            obj.schema_name = pagina
            obj.domain_url = pagina + dominio
            obj.actores = actores
            obj.tipo = tipo
            obj.save()

            messages.success(request, "Entidad registrada correctamente.")
            return redirect('entidad_registro', tipo)

    return render(request, 'entidad_registro.html', {
        'form': form,
        'form2': form2,
        'dominio': dominio,
    })


def listar_entrenadores_nacionales(request):
    pass

def listar_dirigentes_nacionales(request):
    pass

def listar_deportistas_nacionales(request):
    pass

def listar_escenarios_nacionales(request):
    pass

def listar_cajas_nacionales(request):
    pass

def listar_cafs_nacionales(request):
    pass

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
@csrf_exempt
def test(request):
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate, login

    if request.method == 'GET':
        username = request.GET['name']
        password = request.GET['pw']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                return JsonResponse({'id': user.id})

    return JsonResponse({'id': None})

from django.db import connection
from django.contrib.contenttypes.models import ContentType
from snd.modelos.cafs import *
def cafs(request):
    entidad = Entidad.objects.get(schema_name='cliente1')
    connection.set_tenant(entidad)
    centros = CentroAcondicionamiento.objects.all()
    datos = {'escenarios':[], 'cafs':[]} # [Escenarios, CAFS]
    for i in centros:
        dato = {
            'id': i.id,
            'nombre': i.nombre,
            'latitud': i.latitud,
            'longitud': i.longitud,
            'sincronizar': False,
        }
        datos['cafs'].append(dato)
    return JsonResponse(datos)

def actualizarLocalizacionCaf(actor):
    centro = CentroAcondicionamiento.objects.get(id=actor['id'])
    centro.latitud = actor['latitud']
    centro.longitud = actor['longitud']
    centro.save()

import json
def actualizarLocalizacion(request):
    if request.method == 'GET':
        entidad = Entidad.objects.get(schema_name='cliente1')
        connection.set_tenant(entidad)

        tipoActor = request.GET['tipoActor']
        actor = json.loads(request.GET['actor'])

        if tipoActor == '1':
            actualizarLocalizacionCaf(actor)
            return JsonResponse({'response': True})

def sincronizar(request):
    if request.method == 'GET':
        entidad = Entidad.objects.get(schema_name='cliente1')
        connection.set_tenant(entidad)

        escenarios = json.loads(request.GET.get('escenarios', '[]'))
        cafs = json.loads(request.GET.get('cafs', '[]'))

        for i in cafs:
            actualizarLocalizacionCaf(i)

        return JsonResponse({'response': True})
