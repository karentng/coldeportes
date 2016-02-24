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
            request.session['identidad'] = {
                'id_solicitud': nueva_solicitud.id,
                'id_entidad': entidad.id,
                'estado': True
            }
            return redirect('adjuntar_archivo_solicitud',nueva_solicitud.id)
    return render(request,'wizard/wizard_solicitud.html',{
        'form': form,
        'wizard_stage': 1
    })
#Restringir acceso despues de enviada la solicitud para no enviar mas adjuntos durante el proceso
@login_required
def adjuntar_archivo_solicitud(request,id):
    """
    Febrero 19,2016
    Autor: Daniel Correa

    Permite adjuntar archivos a las solicitudes que estan en actual creacion. se verifica la autenticidad de la peticion
    :param id: id de la solicitud a la que se van a adjuntar archivos
    """
    try:
        solicitud = SolicitudEscenario.objects.get(id=id)
    except:
        messages.error(request,'Solicitud no encontrada')
        return redirect('listar_solicitudes')

    #Se verifica la autenticidad de la solicitud
    try:
        auth = request.session['identidad']
        if not auth['estado'] or auth['id_solicitud'] != int(id) or auth['id_entidad'] != request.tenant.id:
            raise Exception
    except Exception:
        messages.error(request,'Estas intentando editar una solicitud que ya fue enviada')
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
    """
    Febrero 19, 2016
    Autor: Daniel Correa

    Permite borrar archivos adjuntos de una solicitud en creacion. se valida la autenticidad de la peticion

    :param id_sol: id de la solicitud a borrar adjunto
    :param id_adj: id del adjunto a borrar
    """
    try:
        adjunto = AdjuntoSolicitud.objects.get(id=id_adj,solicitud=id_sol)
    except Exception:
        messages.error(request,'No existe el archivo adjunto, no se ha realizado ninguna accion')
        return redirect('adjuntar_archivo_solicitud',id_sol)

    #Se verifica la autenticidad de la solicitud
    try:
        auth = request.session['identidad']
        if not auth['estado'] or auth['id_solicitud'] != int(id_sol) or auth['id_entidad'] != request.tenant.id:
            raise Exception
    except Exception:
        messages.error(request,'Estas intentando editar una solicitud que ya fue enviada')
        return redirect('listar_solicitudes')

    adjunto.delete()
    messages.success(request,'Archivo adjunto eliminado satisfactoriamente')
    return redirect('adjuntar_archivo_solicitud',id_sol)


@login_required
def finalizar_solicitud(request,id):
    """
    Febrero 19, 2016
    Autor: Daniel Correa

    Permite finalizar la sesion de creacion de solicitud. informa y redirecciona

    :param id: id de la solicitud en creacion
    """
    try:
        solicitud = SolicitudEscenario.objects.get(id=id)
        messages.success(request,'Solicitud enviada con éxito a:'+str(solicitud.para_quien))
        del request.session['identidad']
    except:
        messages.error(request,'Solicitud no encontrada')

    return redirect('listar_solicitudes')

@login_required
def listar_solicitudes(request):
    solicitudes = SolicitudEscenario.objects.all()
    for s in solicitudes:
        s.codigo = s.codigo_unico(request.tenant)
    return render(request,'lista_mis_solicitudes.html',{
        'solicitudes': solicitudes
    })

@login_required
def cancelar_solicitud(request, id=None):
    """
    Febrero 19, 2016
    Autor: Daniel Correa

    Permite cancelar una solicitud al momento de estarse creando o luego de estar creada
    :param request:
    :param id:
    :return:
    """
    if id:
        try:
            solicitud = SolicitudEscenario.objects.get(id=id)
        except Exception:
            messages.error(request,'No existe la solicitud, proceso no realizado')
        solicitud.estado = 4
        solicitud.save()
    messages.warning(request,'Solicitud cancelada correctamente')
    return redirect('listar_solicitudes')

@login_required
def imprimir_solicitud(request,id):
    return render(request,'solicitud_imprimir.html',{

    })