from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from solicitudes_escenarios.solicitud.forms import SolicitudEscenarioForm
from solicitudes_escenarios.respuesta.models import ListaSolicitudes
from django.db import connection
from django.contrib import messages
# Create your views here.

@login_required
def generar_solicitud(request):
    """
    Febrero 19, 2016
    Autor: Daniel Correa

    Permite crear una solicitud con sus datos basicos
    """
    form = SolicitudEscenarioForm()
    if request.method == 'POST':
        entidad = request.tenant
        form = SolicitudEscenarioForm(request.POST)
        if form.is_valid():
            nueva_solicitud = form.save()
            connection.set_tenant(nueva_solicitud.para_quien)
            ListaSolicitudes.objects.create(solicitud=nueva_solicitud.id,entidad_solicitante=entidad).save()
            connection.set_tenant(entidad)
            messages.success(request,'Solicitud enviada con éxito a:'+str(nueva_solicitud.para_quien))
            return redirect('listar_solicitudes')

    return render(request,'generar_solicitud.html',{
        'form' : form
    })

@login_required
def listar_solicitudes(request):
    return HttpResponse('Hola mundo')