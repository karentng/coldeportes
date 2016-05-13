from django.shortcuts import render, redirect
from snd.modelos.escenarios import Escenario
from reserva_escenarios.models import ReservaEscenario
from reserva_escenarios.forms import SolicitarReservaForm

# Create your views here.
def listar_escenarios(request):

    escenarios = Escenario.objects.all()

    return render(request,'lista_escenarios.html',{
        'escenarios': escenarios

    })


def agendar_reserva(request, escenario_id):

    escenario = Escenario.objects.get(id = escenario_id)
    reservas = ReservaEscenario.objects.filter(escenario = escenario_id, aprobada = True)

    return render(request,'calendario_reservas.html',{
        'reservas': reservas,
        'escenario': escenario
    })


def solicitar_reserva(request, escenario_id):

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
