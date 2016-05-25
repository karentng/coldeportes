from datetime import datetime
from django.shortcuts import render, redirect
from snd.modelos.escenarios import Escenario
from reserva_escenarios.models import ReservaEscenario, ConfiguracionReservaEscenario
from reserva_escenarios.forms import SolicitarReservaForm, ConfiguracionReservaEscenarioForm

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


def agendar_reserva(request, escenario_id):
    """
    Mayo 18, 2016
    Autor: Karent Narvaez

    Permite visualizar el calendario de reservas de un escenario
    """

    escenario = Escenario.objects.get(id = escenario_id)
    reservas = ReservaEscenario.objects.filter(escenario = escenario_id, aprobada = True)

    return render(request,'calendario_reservas.html',{
        'reservas': reservas,
        'escenario': escenario
    })


def solicitar_reserva(request, escenario_id):
    """
    Mayo 20, 2016
    Autor: Karent Narvaez

    Permite guardar la información de contacto de una reserva
    """

    escenario = Escenario.objects.get(id = escenario_id)
    form = SolicitarReservaForm()

    if request.method == 'POST':
            form = SolicitarReservaForm(request.POST)

            if form.is_valid():
                nueva_solicitud = form.save(commit = False)
                nueva_solicitud.escenario = escenario
                nueva_solicitud.save()
                #return redirect('adjuntar_requerimientos_reconocimiento', nueva_solicitud.id)

    return render(request,'solicitar_reserva.html',{
        'form': form,
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
            'message': 'actividad no existe'
        }

        escenario = Escenario.objects.get(id =  escenario_id)

        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_inicio = fecha_inicio.split(" ")
        fecha_inicio = fecha_inicio[:6]
        fecha_inicio = " ".join(fecha_inicio)
        fecha_inicio = datetime.strptime(fecha_inicio, "%a %b %d %Y %H:%M:%S %Z%z")
        #print(fecha_inicio)

        fecha_fin = request.POST.get("fecha_fin")
        if fecha_fin != '':
            fecha_fin = fecha_fin.split(" ")
            fecha_fin = fecha_fin[:6]
            fecha_fin = " ".join(fecha_fin)
            fecha_fin = datetime.strptime(fecha_fin, "%a %b %d %Y %H:%M:%S %Z%z")
        else:
            fecha_fin = fecha_inicio + timedelta(minutes = 120)
            
        #print(fecha_fin)
        

        reserva = ReservaEscenario(escenario = escenario, fecha_inicio = fecha_inicio, fecha_fin = fecha_fin).save()

        return redirect('solicitar_reserva', escenario_id)


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