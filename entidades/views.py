import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from entidades.models import *
from entidades.forms import *
from django.conf import settings
from django.contrib import messages
from snd.modelos.cafs import CentroAcondicionamiento

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

@login_required
def editar(request, idEntidad):
    try:
        entidad = Entidad.objects.get(id=idEntidad)
    except Exception:
        return redirect('entidad_listar')

    form = EntidadEditarForm(instance=entidad)
    form2 = ActoresForm(instance=entidad.actores)

    if request.method == 'POST':
        form = EntidadEditarForm(request.POST, instance=entidad)
        form2 = ActoresForm(request.POST, instance=entidad.actores)
        if form.is_valid() and form2.is_valid():
            actores = form2.save()
            obj = form.save()
            messages.success(request, "Entidad editada correctamente.")
            return redirect('entidad_listar')

    return render(request, 'entidad_editar.html', {
        'form': form,
        'form2': form2,
    })

@login_required
def listar(request):
    entidades = Entidad.objects.exclude(schema_name="public")
    return render(request, 'entidad_listar.html', {
        'entidades': entidades,
    })


from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import connection

@csrf_exempt
def appMovilLogin(request):
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate, login

    if request.method == 'GET':
        username = request.GET['name']
        password = request.GET['pw']
        entidad = request.GET['entidad']

        entidad = Entidad.objects.get(schema_name=entidad)
        connection.set_tenant(entidad)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                return JsonResponse({'id': user.id})

    return JsonResponse({'id': None})

from snd.modelos.cafs import *
from snd.modelos.escenarios import *
def appMovilObtenerActores(request):
    datos = {'escenarios':[], 'cafs':[]} # [Escenarios, CAFS]
    if request.method == 'GET':
        entidad = request.GET.get('entidad')
        entidad = Entidad.objects.get(schema_name=entidad)
        connection.set_tenant(entidad)
        centros = CentroAcondicionamiento.objects.all()
        
        for i in centros:
            dato = {
                'id': i.id,
                'nombre': i.nombre,
                'latitud': i.latitud,
                'longitud': i.longitud,
                'altura': i.altura,
                'sincronizar': False,
            }
            datos['cafs'].append(dato)

        escenarios = Escenario.objects.all()
        for i in escenarios:
            dato = {
                'id': i.id,
                'nombre': i.nombre,
                'latitud': i.latitud,
                'longitud': i.longitud,
                'altura': i.altura,
                'sincronizar': False,
            }
            datos['escenarios'].append(dato)

    return JsonResponse(datos)

def actualizarLocalizacionActor(actor, modelo):
    instancia = modelo.objects.get(id=actor['id'])
    instancia.latitud = actor['latitud']
    instancia.longitud = actor['longitud']
    instancia.altura = actor['altura']
    instancia.save()

import json
def appMovilActualizarLocalizacion(request):
    if request.method == 'GET':
        entidad = request.GET['entidad']
        entidad = Entidad.objects.get(schema_name=entidad)
        connection.set_tenant(entidad)

        tipoActor = request.GET['tipoActor']
        actor = json.loads(request.GET['actor'])

        if tipoActor == '1':
            actualizarLocalizacionActor(actor, CentroAcondicionamiento)
            return JsonResponse({'response': True})

        if tipoActor == '0':
            actualizarLocalizacionActor(actor, Escenario)
            return JsonResponse({'response': True})

def appMovilSincronizar(request):
    if request.method == 'GET':
        entidad = request.GET.get('entidad')
        entidad = Entidad.objects.get(schema_name=entidad)
        connection.set_tenant(entidad)

        escenarios = json.loads(request.GET.get('escenarios', '[]'))
        cafs = json.loads(request.GET.get('cafs', '[]'))

        for i in cafs:
            actualizarLocalizacionActor(i, CentroAcondicionamiento)

        for i in escenarios:
            actualizarLocalizacionActor(i, Escenario)

        return JsonResponse({'response': True})