from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse
from .forms import CalendarioForm
from django.contrib import messages
from django.db import connection
from entidades.models import Entidad,CalendarioNacional
# Create your views here.
def cargar_calendario(request):

    return render(request,'calendario.html',{

    })

@login_required
def registro_calendario(request):
    form = CalendarioForm()
    if request.method == 'POST':
        yo = request.tenant
        public = Entidad.objects.get(schema_name='public')
        connection.set_tenant(public)
        form = CalendarioForm(request.POST)
        ev = form.save(commit=False)
        ev.entidad = yo
        ev.save()
        connection.set_tenant(yo)
        messages.success(request, "El evento a sido enviado al Calendario Deportivo Nacional con exito!")
        return redirect('listado_calendario_nacional')
    return render(request,'registro_calendario.html',{
        'form': form
    })

@login_required
def listar_eventos(request):
    yo = request.tenant
    public = Entidad.objects.get(schema_name='public')
    connection.set_tenant(public)
    eventos = CalendarioNacional.objects.filter(entidad=yo)
    connection.set_tenant(yo)
    return render(request,'lista_eventos_calendario.html',{
        'eventos':eventos
    })

def public(request):
    return HttpResponse("Public si señor")

def tenant(request):
    return HttpResponse("Tenant no señor")