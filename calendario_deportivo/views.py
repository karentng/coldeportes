from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse
from .forms import CalendarioForm
from django.contrib import messages
from django.db import connection
from entidades.models import Entidad,CalendarioNacional
# Create your views here.

#Vistas de Registro para Federacion

@login_required
@permission_required('entidades.add_calendarionacional')
def registro_calendario(request,id=None):

    if id:
        try:
            evento = CalendarioNacional.objects.get(id=id)
            if evento.estado != 2:
                raise Exception
        except:
            messages.error(request,'El evento no exite o intentas editar un evento que no esta disponible')
            return redirect('listado_calendario_nacional')

        editar = True
        deporte_id = evento.deporte.id
    else:
        deporte_id = None
        evento = None
        editar = False

    form = CalendarioForm(instance=evento,deporte_id=deporte_id)
    if request.method == 'POST':
        yo = request.tenant
        public = Entidad.objects.get(schema_name='public')
        connection.set_tenant(public)
        deporte_id = request.POST['deporte']
        form = CalendarioForm(request.POST,instance=evento,deporte_id=deporte_id)
        if form.is_valid():
            ev = form.save(commit=False)
            ev.entidad = yo
            ev.save()
            connection.set_tenant(yo)
            messages.success(request, "El evento a sido enviado al Calendario Deportivo Nacional con exito!, Aparecera cuando COLDEPORTES lo apruebe")
            return redirect('listado_calendario_nacional')
        connection.set_tenant(yo)
    return render(request,'registro_calendario.html',{
        'form': form,
        'edicion':editar
    })

@login_required
@permission_required('entidades.add_calendarionacional')
def listar_eventos(request):
    yo = request.tenant
    public = Entidad.objects.get(schema_name='public')
    connection.set_tenant(public)
    eventos = CalendarioNacional.objects.filter(entidad=yo)
    connection.set_tenant(yo)
    return render(request,'lista_eventos_calendario.html',{
        'eventos':eventos
    })

@login_required
@permission_required('entidades.add_calendarionacional')
def cancelar_evento(request,id):
    yo = request.tenant
    public = Entidad.objects.get(schema_name='public')
    connection.set_tenant(public)
    try:
        evento = CalendarioNacional.objects.get(id=id,entidad=yo)
        evento.estado = 3
        evento.save()
        messages.warning(request,'El evento ha sido cancelado correctamente')
    except:
        messages.error(request,'El evento que intenta cancelar no existe')
    connection.set_tenant(yo)
    return redirect('listado_calendario_nacional')

@login_required
@permission_required('entidades.add_calendarionacional')
def ver_evento(request,id):
    yo = request.tenant
    public = Entidad.objects.get(schema_name='public')
    connection.set_tenant(public)
    try:
        evento = CalendarioNacional.objects.get(id=id)
    except:
        messages.error(request,'El evento solicitado no existe')
        return redirect('listado_calendario_nacional')
    connection.set_tenant(yo)
    return render(request,'ver_evento_calendario.html',{
        'evento':evento
    })

#Vistas para tenant nacional
def cargar_calendario(request):
    eventos = CalendarioNacional.objects.filter(estado=0)
    colores = ['bg-purple','bg-blue','bg-green','bg-red','bg-yellow-darker','bg-blue-darker','bg-black','bg-red-darker','bg-green-darker']
    i=0
    for e in eventos:
        e.color = colores[i]
        i+=1
        if i==9:
            i=0
    return render(request,'calendario.html',{
        'eventos':eventos
    })

@login_required
def listar_todos_calendario(request):
    eventos = CalendarioNacional.objects.all()
    return render(request,'aprobar_calendario.html',{
        'eventos':eventos
    })

@login_required
def listar_pendientes_calendario(request):
    eventos = CalendarioNacional.objects.filter(estado=2)
    return render(request,'aprobar_calendario.html',{
        'eventos':eventos
    })

@login_required
def aprobar_evento(request,id):
    try:
        evento = CalendarioNacional.objects.get(id=id)
    except:
        messages.error(request,'El evento solicitado no existe')
        return redirect('listar_aprobar_calendario')

    evento.estado = 0
    evento.save()
    messages.success(request,'El evento ha sido aprobado con exito!')
    return redirect('listar_aprobar_calendario')

@login_required
def reprobar_evento(request,id):
    try:
        evento = CalendarioNacional.objects.get(id=id)
    except:
        messages.error(request,'El evento solicitado no existe')
        return redirect('listar_aprobar_calendario')

    evento.estado = 1
    evento.save()
    messages.warning(request,'El evento ha sido rechazado con exito')
    return redirect('listar_aprobar_calendario')

def ver_evento_nacional(request,id):
    try:
        evento = CalendarioNacional.objects.get(id=id)
    except:
        messages.error(request,'El evento solicitado no existe')
        return redirect('cargar_calendario_nacional')

    return render(request,'ver_evento_calendario.html',{
        'evento':evento
    })