from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
# Create your views here.
@login_required
def generar_transferencia(request,tipo_transfer,tipo_persona,id):
    """
    Julio 15, 2015
    Autor: Daniel Correa

    Transferencia de objetos entre entidades, esta definida la transferencia de personas (Deportistas, Dirigentes, Entrenadores) y Escenarios
    Dentro de personas el protocolo es , 1 para Deportistas, 2 para Dirigentes y 3 para Enetrenadores

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param tipo_transfer: Tipo de transferencia, el protocolo define 1 para personas y 2 para escenarios
    :type tipo_transfer: int
    :param tipo_persona: Tipo de persona, el protocolo define 1 para Deportistas, 2 para Dirigentes y 3 para Enetrenadores
    :type tipo_persona: int
    :param id: Identificacion de objeto a tranferir
    :type id: String
    """

    if tipo_transfer==1:
        #Transferencia de personas
        pass
    elif tipo_transfer==2:
        #Transferencia de escenarios
        pass
    return render(request,'generar_transferencia.html',{})

@login_required
def procesar_transferencia(request,tipo_transfer,tipo_persona,id):
    pass