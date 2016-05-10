from django.shortcuts import render, redirect
from snd.modelos.escenarios import Escenario

# Create your views here.
def listar_escenarios(request):

    escenarios = Escenario.objects.all()

    return render(request,'lista_escenarios.html',{
        'escenarios': escenarios

    })