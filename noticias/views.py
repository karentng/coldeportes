from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from .forms import NoticiaForm
from .models import Noticia
import datetime


# Create your views here.
@login_required
@permission_required('noticias.add_noticia')
def registrar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)

        if form.is_valid():

            noticia = form.save(commit=False)
            nueva_foto = request.POST.get('imagen-crop')

            if nueva_foto == "No":
                noticia.foto = ""
            else:
                noticia.foto = nueva_foto

            if noticia.video:
                noticia.video = noticia.video.replace("watch?v=", "embed/")

            noticia.previsualizacion = request.POST.get("previsualizacion")
            noticia.etiquetas = noticia.etiquetas.upper()
            form.save()
            messages.success(request, 'Se ha registrado la noticia correctamente')
            return redirect('listar_noticias')
    else:
        form = NoticiaForm()
    return render(request, 'registrar_noticia.html', {'form': form})


def listar_noticias(request):
    from django.db.models import Q
    user = request.user
    if user.has_perm("publicidad.change_clasificado"):
        noticias = Noticia.objects.all()
    else:
        noticias = Noticia.objects.filter(Q(fecha_inicio__lte=datetime.date.today()) &
                                          Q(fecha_expiracion__gte=datetime.date.today()), estado=1)

    return render(request, 'listar_noticias.html', {'noticias': noticias})


def detalles_noticia(request, id_noticia):
    try:
        noticia = Noticia.objects.get(id=id_noticia)
    except Exception:
        messages.error(request, 'La noticia que está tratando de visualizar no existe')
        return redirect('listar_noticias')
    if not request.user.has_perm("publicidad.change_clasificado"):
        if noticia.fecha_inicio > datetime.date.today() or noticia.fecha_expiracion < datetime.date.today() or noticia.estado == 0:
            messages.error(request, 'La noticia que está tratando de visualizar no está disponible')
            return redirect('listar_noticias')

    return render(request, 'detalles_noticia.html', {'noticia': noticia})


@login_required
@permission_required('noticias.change_noticia')
def editar_noticia(request, id_noticia):
    try:
        noticia = Noticia.objects.get(id=id_noticia)
    except Exception:
        messages.error(request, 'La noticia que está intentando editar no existe')
        return redirect('listar_noticias')

    form = NoticiaForm(instance=noticia)

    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        nueva_foto = request.POST.get("imagen-crop")
        if form.has_changed or nueva_foto != "No":
            if form.is_valid():
                noticia = form.save(commit=False)
                nueva_foto = request.POST.get('imagen-crop')

                if nueva_foto == "No":
                    noticia.foto = ""
                elif nueva_foto != "si":
                    noticia.foto = nueva_foto

                if noticia.video:
                    noticia.video = noticia.video.replace("watch?v=", "embed/")

                noticia.previsualizacion = request.POST.get("previsualizacion")
                noticia.etiquetas = noticia.etiquetas.upper()
                form.save()

                messages.success(request, 'La noticia se ha editado correctamente')
                return redirect('listar_noticias')
    return render(request, 'registrar_noticia.html', {'form': form,
                                                      'edicion': True, 'foto': noticia.foto})


@login_required
@permission_required('noticias.change_noticia')
def cambiar_estado_noticia(request, id_noticia):
    try:
        noticia = Noticia.objects.get(id=id_noticia)
        noticia.estado = not noticia.estado
        noticia.save()

    except Exception:
        messages.error(request, 'La noticia que está intentando eliminar no existe')
        return redirect('listar_noticias')

    messages.success(request, 'Se ha eliminado la noticia correctamente')
    return redirect('listar_noticias')

