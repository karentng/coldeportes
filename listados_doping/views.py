from django.shortcuts import render, redirect
from .models import CasoDoping
from .forms import CasoDopingForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from reportes.models import TenantDeportistaView,TenantPersonalApoyoView,TenantDirigenteView
from django.http import JsonResponse,HttpResponseNotFound



# Create your views here.
@login_required
@permission_required('listados_doping.add_casodoping')
def registrar_caso_doping(request):
    if request.method == 'POST':
        form = CasoDopingForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha registrado el caso de doping correctamente')
            return redirect('listar_casos_doping')
    else:
        form = CasoDopingForm()
    return render(request, 'registrar_caso_doping.html', {'form': form})


@login_required
@permission_required('listados_doping.change_casodoping')
def editar_caso_doping(request, id_caso_doping):
    try:
        caso_doping = CasoDoping.objects.get(id=id_caso_doping)
    except Exception:
        messages.error(request, 'El caso de doping que está intentando editar no existe')
        return redirect('listar_casos_doping')

    form = CasoDopingForm(instance=caso_doping)

    if request.method == 'POST':
        form = CasoDopingForm(request.POST, instance=caso_doping)
        if form.has_changed:
            if form.is_valid():
                form.save()
                messages.success(request, 'El caso de doping se ha editado correctamente')
                return redirect('listar_casos_doping')
    return render(request, 'registrar_caso_doping.html', {'form': form,
                                                          'edicion':True})


def listar_casos_doping(request):
    if request.user.has_perm("listados_doping.change_casodoping"):
        casos_doping = CasoDoping.objects.all()
    else:
        casos_doping = CasoDoping.objects.filter(estado=0)

    return render(request, 'listar_casos_doping.html', {'casos_doping': casos_doping})


@login_required
@permission_required('listados_doping.change_casodoping')
def cambiar_estado_caso_doping(request, id_caso_doping):
    try:
        caso_doping = CasoDoping.objects.get(id=id_caso_doping)
        caso_doping.estado = not caso_doping.estado
        caso_doping.save()

    except Exception:
        messages.error(request, 'El caso de doping que está intentando cambiar de estado no existe')
        return redirect('listar_casos_doping')

    messages.success(request, 'Se ha cambiado el estado del caso de doping correctamente')
    return redirect('listar_casos_doping')


@login_required
@permission_required('listados_doping.add_casodoping')
def busqueda_persona_sistema(request,id_persona):
    if request.is_ajax():
        dirigente = TenantDirigenteView.objects.filter(identificacion=id_persona)
        deportista = TenantDeportistaView.objects.filter(identificacion=id_persona)
        personal_apoyo = TenantPersonalApoyoView.objects.filter(identificacion=id_persona)

        if dirigente:
            persona = dirigente[0]
        elif deportista:
            persona = deportista[0]
        elif personal_apoyo:
            persona = personal_apoyo[0]
        else:
            persona = None

        if persona:
            datos = {
                'identificacion':id_persona,
                'nombres': persona.nombres,
                'apellidos': persona.apellidos,
            }
            return JsonResponse(datos)
        else:
            return HttpResponseNotFound()