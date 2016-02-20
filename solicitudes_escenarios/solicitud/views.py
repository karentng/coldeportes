from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from solicitudes_escenarios.solicitud.forms import SolicitudEscenarioForm,AdjuntoSolicitudForm
from solicitudes_escenarios.respuesta.models import ListaSolicitudes
from solicitudes_escenarios.solicitud.models import SolicitudEscenario,AdjuntoSolicitud
from django.db import connection
from django.contrib import messages
# Create your views here.

@login_required
def generar_solicitud(request,id=None):
    """
    Febrero 19, 2016
    Autor: Daniel Correa

    Permite crear una solicitud con sus datos basicos
    """
    try:
        sol = SolicitudEscenario.objects.get(id=id)
    except Exception:
        sol = None

    form = SolicitudEscenarioForm(instance=sol)
    if request.method == 'POST':
        entidad = request.tenant
        form = SolicitudEscenarioForm(request.POST,instance=sol)
        if form.is_valid():
            nueva_solicitud = form.save()
            connection.set_tenant(nueva_solicitud.para_quien)
            ListaSolicitudes.objects.create(solicitud=nueva_solicitud.id,entidad_solicitante=entidad).save()
            connection.set_tenant(entidad)
            return redirect('adjuntar_archivo_solicitud',nueva_solicitud.id)
    return render(request,'wizard/wizard_solicitud.html',{
        'form': form,
        'wizard_stage': 1
    })
#Restringir acceso despues de enviada la solicitud para no enviar mas adjuntos durante el proceso
@login_required
def adjuntar_archivo_solicitud(request,id):
    try:
        solicitud = SolicitudEscenario.objects.get(id=id)
    except:
        messages.error(request,'Solicitud no encontrada')
        return redirect('listar_solicitudes')

    form = AdjuntoSolicitudForm()

    if request.method == 'POST':
        form = AdjuntoSolicitudForm(request.POST,request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.solicitud = solicitud
            ad.save()
            return redirect('adjuntar_archivo_solicitud',solicitud.id)
    return render(request,'wizard/wizard_adjuntos.html',{
        'form' : form,
        'sol_id': id,
        'wizard_stage': 2,
        'adjuntos': solicitud.adjuntos()
    })

@login_required
def borrar_adjunto(request,id_sol,id_adj):
    try:
        adjunto = AdjuntoSolicitud.objects.get(id=id_adj,solicitud=id_sol)
    except Exception:
        messages.error(request,'No existe el archivo adjunto, no se ha realizado ninguna accion')
        return redirect('adjuntar_archivo_solicitud',id_sol)

    adjunto.delete()
    messages.success(request,'Archivo adjunto eliminado satisfactoriamente')
    return redirect('adjuntar_archivo_solicitud',id_sol)


@login_required
def finalizar_solicitud(request,id):
    try:
        solicitud = SolicitudEscenario.objects.get(id=id)
        messages.success(request,'Solicitud enviada con éxito a:'+str(solicitud.para_quien))
    except:
        messages.error(request,'Solicitud no encontrada')

    return redirect('listar_solicitudes')

@login_required
def listar_solicitudes(request):
    return HttpResponse('Hola mundo')

@login_required
def cancelar_solicitud(request, id=None):
    if id:
        try:
            solicitud = SolicitudEscenario.objects.get(id=id)
        except Exception:
            messages.error(request,'No existe la solicitud, proceso no realizado')
        solicitud.estado = 4
        solicitud.save()
    messages.warning(request,'Solicitud cancelada correctamente')
    return redirect('listar_solicitudes')