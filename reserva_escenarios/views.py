from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from snd.modelos.escenarios import Escenario
from reserva_escenarios.models import ReservaEscenario, ConfiguracionReservaEscenario
from reserva_escenarios.forms import SolicitarReservaForm, ConfiguracionReservaEscenarioForm, ResponderSolicitudReservaForm


# Create your views here.
def listar_escenarios(request):
    """
    Mayo 05, 2016
    Autor: Karent Narvaez

    Permite listar los escenarios deportivos del tenant
    """

    escenarios = Escenario.objects.all()

    return render(request,'lista_escenarios.html',{
        'escenarios': escenarios

    })


def listar_solicitudes(request):
    """
    Mayo 25, 2016
    Autor: Karent Narvaez

    Permite listar las solicitudes de reservas de escenarios
    """

    solicitudes = ReservaEscenario.objects.filter(estado = 2).exclude(correo_solicitante = '')
    dashboard = dict()
    dashboard['total_solicitudes'] = ReservaEscenario.objects.exclude(correo_solicitante = '').count() or 0
    dashboard['total_rechazadas'] = ReservaEscenario.objects.filter(estado = 3).count() or 0
    dashboard['total_aprobadas'] = ReservaEscenario.objects.filter(estado = 1).count() or 0
    dashboard['total_esperando_respuesta'] = solicitudes.count() or 0

    return render(request,'lista_solicitudes.html',{
        'solicitudes': solicitudes,
        'dashboard': dashboard

    })


def agendar_reserva(request, escenario_id):
    """
    Mayo 18, 2016
    Autor: Karent Narvaez

    Permite visualizar el calendario de reservas de un escenario
    """

    escenario = Escenario.objects.get(id = escenario_id)
    reservas = ReservaEscenario.objects.filter(escenario = escenario_id, estado = 1)

    return render(request,'calendario_reservas.html',{
        'reservas': reservas,
        'escenario': escenario
    })


def solicitar_reserva(request):
    """
    Mayo 20, 2016
    Autor: Karent Narvaez

    Permite guardar la información de contacto de una reserva
    """

    try:
        reserva = ReservaEscenario.objects.get(id = request.session['reserva_id'])
    except Exception as e:
        print(e)

    form = SolicitarReservaForm(instance = reserva)
    reserva.codigo_unico = reserva.codigo_unico(request.tenant)

    if request.method == 'POST':
            form = SolicitarReservaForm(request.POST, instance = reserva)

            if form.is_valid():
                nueva_solicitud = form.save(commit = False)
                nueva_solicitud.save()
                messages.success(request, "La reserva ha sido enviada al administrador del escenario con éxito. Aparecerá en el calendario si es aprobada y usted recibirá notificación.")
                return redirect('listar_escenarios_reservas')

    return render(request,'solicitar_reserva.html',{
        'form': form,
        'reserva': reserva
    })


def guardar_fechas_reserva(request, escenario_id):
    """
    Mayo 23, 2016
    Autor: Karent Narvaez

    Permite guardar las fechas de una reserva de un escenario
    """
    if request.is_ajax():

        response = {
            'status': 'error',
            'message': 'Escenario no existe.'
        }
        try:
            escenario = Escenario.objects.get(id = escenario_id)
        except Exception:
            return JsonResponse(response)

        try:
            fecha_inicio = request.POST.get("fecha_inicio")
            fecha_inicio = fecha_inicio.split(" ")
            fecha_inicio = fecha_inicio[:6]
            fecha_inicio = " ".join(fecha_inicio)
            fecha_inicio = datetime.strptime(fecha_inicio, "%a %b %d %Y %H:%M:%S %Z%z")

            fecha_fin = request.POST.get("fecha_fin")
            if fecha_fin:
                fecha_fin = fecha_fin.split(" ")
                fecha_fin = fecha_fin[:6]
                fecha_fin = " ".join(fecha_fin)
                fecha_fin = datetime.strptime(fecha_fin, "%a %b %d %Y %H:%M:%S %Z%z")
            else:
                fecha_fin = fecha_inicio + timedelta(minutes = 120)        

            reserva = ReservaEscenario.objects.create(escenario = escenario, fecha_inicio = fecha_inicio, fecha_fin = fecha_fin, estado = 2)
            reserva.save()
            request.session["reserva_id"] = reserva.id
            message = "Reserva creada correctamente."
            
        except Exception as e:
            print(e)
            message = e

        response = {
            'status': 'error',
            'message': message
        }

        return JsonResponse(response)


def configurar_reservas(request, escenario_id):
    """
    Mayo 24, 2016
    Autor: Karent Narvaez

    Permite crear o editar una configuración de las reservas de un escenario
    """
    escenario = Escenario.objects.get(id = escenario_id)
    try:
        configuracion = ConfiguracionReservaEscenario.objects.get(escenario = escenario_id)
    except Exception as e:
        configuracion = None

    form = ConfiguracionReservaEscenarioForm(instance = configuracion)

    if request.method == 'POST':
        form = ConfiguracionReservaEscenarioForm(request.POST, instance = configuracion)

        if form.is_valid():
            nueva_configuracion = form.save(commit = False)
            nueva_configuracion.escenario = escenario
            nueva_configuracion.save()
            return redirect('listar_escenarios_reservas')

    return render(request,'configuracion_reserva.html',{
        'form': form
    })


def responder_solicitud(request, solicitud_id):
    """
    Mayo 25, 2016
    Autor: Karent Narvaez

    Permite cargar la información de la solicitud de reserva y el formulario para responder.

    """
    solicitud = ReservaEscenario.objects.get(id = solicitud_id)
    solicitud.codigo_unico = solicitud.codigo_unico(request.tenant)

    form = ResponderSolicitudReservaForm(instance = solicitud)

    if request.method == 'POST':
        form = ResponderSolicitudReservaForm(request.POST, instance = solicitud)

        if form.is_valid():
            form.save()
            messages.success(request, 'La respuesta se almacenado correctamente. Se enviará un correo electrónico al solicitante.')
            return redirect('listar_escenarios_reservas')

    return render(request,'responder_solicitud.html',{
        'solicitud' : solicitud,
        'form' : form,
        'responder': True
    })



@login_required
def imprimir_solicitud(request, reserva_id):
    """
    Mayo 26, 2016
    Autor: Karent Narvaez

    Permite renderizar el html imprimible de la solicitud de reserva|

    """
    try:
        solicitud = ReservaEscenario.objects.get(id = reserva_id)
    except:
        messages.error(request,'No existe la solicitud')
        return redirect('listar_solicitudes_reservas')

    solicitud.codigo_unico = solicitud.codigo_unico(request.tenant)

    return render(request,'imprimir_solicitud.html',{
        'solicitud' : solicitud,
    })