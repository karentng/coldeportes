from django.shortcuts import render
from .models import CasoDoping

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

    if user.has_perm("listados_doping.change_casodoping"):
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