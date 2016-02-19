from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from solicitudes_escenarios.solicitud.forms import SolicitudEscenarioForm
# Create your views here.

@login_required
def generar_solicitud(request):
    form = SolicitudEscenarioForm()

    return render(request,'generar_solicitud.html',{
        'form' : form
    })

@login_required
def listar_solicitudes(request):
    return HttpResponse('Hola mundo')