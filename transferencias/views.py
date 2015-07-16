from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from entidades.models import Entidad
from snd.models import Deportista,Escenario,Entrenador
from .forms import TransferenciaForm
# Create your views here.
@login_required
def generar_transferencia(request,tipo_transfer,tipo_persona,id):
    """
    Julio 15, 2015
    Autor: Daniel Correa

    Transferencia de objetos entre entidades, esta definida la transferencia de personas (Deportistas, Entrenadores) y Escenarios
    Dentro de personas el protocolo es , 1 para Deportistas y 2 para Enetrenadores

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param tipo_transfer: Tipo de transferencia, el protocolo define 1 para personas y 2 para escenarios
    :type tipo_transfer: int
    :param tipo_persona: Tipo de persona, el protocolo define 1 para Deportistas y 2 para Enetrenadores
    :type tipo_persona: int
    :param id: Identificacion de objeto a tranferir
    :type id: String
    """
    objeto = None
    entidad_solicitante = request.tenant
    entidades = Entidad.objects.exclude(nombre__in=['publico',entidad_solicitante.nombre])
    if tipo_transfer==1: #Transferencia de personas
        if tipo_persona==1: #Transferencia de deportistas
            objeto = Deportista.objects.get(id=id)
        elif tipo_persona==2: #Transferencia de entrenadores
            objeto = Entrenador.objects.get(id=id)
    elif tipo_transfer==2: #Transferencia de escenarios
        objeto = Escenario.objects.get(id=id)

    if request.method == 'POST':
        #trans_form = TransferenciaForm(request.POST)
        #entidad_cambio = trans_form.cleaned_data['entidad']
        #print(entidad_cambio)
        #connection.set_tenant(entidad)
        #ContentType.objects.clear_cache()
        pass

    return render(request,'generar_transferencia.html',{
        'entidades' : entidades,
        'objeto' : objeto
    })

@login_required
def procesar_transferencia(request,tipo_transfer,tipo_persona,id):
    pass