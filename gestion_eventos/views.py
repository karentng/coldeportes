from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from .forms import *
from .models import Evento
from noticias.models import Noticia
from noticias.forms import NoticiaForm
from snd.formularios.deportistas import VerificarExistenciaForm
from snd.views.deportistas import existencia_deportista
from datetime import datetime


# Create your views here.
@login_required
# @permission_required('gestion_eventos.add_evento')
def registrar_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)

        if form.is_valid():
            evento = form.save(commit=False)
            nueva_foto = request.POST.get('imagen-crop')

            if nueva_foto == "No":
                evento.imagen = ""
            else:
                evento.imagen = nueva_foto

            if evento.video:
                evento.video = evento.video.replace("watch?v=", "embed/")
            evento.previsualizacion = request.POST.get("previsualizacion")
            evento.cupo_disponible = evento.cupo_participantes

            noticia_evento = Noticia()
            noticia_evento.titulo = evento.titulo_evento
            noticia_evento.cuerpo_noticia = evento.descripcion_evento
            noticia_evento.fecha_inicio = datetime.date.today()
            noticia_evento.fecha_expiracion = evento.fecha_finalizacion
            noticia_evento.autor = evento.autor
            noticia_evento.foto = evento.imagen
            noticia_evento.video = evento.video
            noticia_evento.etiquetas = ""
            noticia_evento.save()
            evento.noticia = noticia_evento
            evento.save()
            messages.success(request, 'Se ha registrado el evento correctamente')
            return redirect('listar_eventos')
    else:
        form = EventoForm()
    return render(request, 'registrar_evento.html', {'form': form})


def listar_eventos(request):
    from django.db.models import Q
    # if user.has_perm("gestion_eventos.change_evento"):
    if True:
        eventos = Evento.objects.all()
    else:
        eventos = Evento.objects.filter(Q(fecha_inicio__lte=datetime.date.today()) &
                                        Q(fecha_finalizacion__gte=datetime.date.today()), estado=1)

    return render(request, 'listar_eventos.html', {'eventos': eventos})


def listar_participantes(request, id_evento):
    if True:
        try:
            eventos = Evento.objects.get(id=id_evento)
            participantes = eventos.participantes
        except Exception:
            messages.error(request, 'El evento al que trata de acceder no existe!')
            return redirect('listar_eventos')
    else:
        participantes = None
        eventos = None

    return render(request, 'listar_participantes.html', {'participantes': participantes})


def preinscripcion_evento(request, id_evento):

    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        messages.error(request, 'El evento al que trata de acceder no existe!')
        return redirect('listar_eventos')
    try:
        datos = request.session["datos"]
    except Exception:
        return redirect('verificar_participante')

    participante_form = ParticipanteForm(initial=datos)
    if request.method == 'POST':
        participante_form = ParticipanteForm(request.POST)
        if participante_form.is_valid():
            participante = participante_form.save(commit=False)
            participante.evento_participe = evento.id
            participante.save()
            evento.participantes.add(participante)
            evento.cupo_disponible = evento.cupo_disponible - 1
            evento.save()
            messages.success(request, "Has sido preinscrito con exito!")
            return redirect('listar_eventos')

    return render(request, 'registrar_preinscrito.html', {'form': participante_form})


def verificar_participante(request,id_evento):

    try:
        evento = Evento.objects.get(id=id_evento)
        if evento.cupo_disponible == 0:
            messages.success(request, 'No hay cupos disponibles para el evento!')
            return redirect('listar_eventos')
    except Exception:
        messages.success(request, 'El evento al que trata de acceder no existe!')
        return redirect('listar_eventos')

    if request.method=='POST':
        form = VerificarExistenciaForm(request.POST)

        if form.is_valid():
            datos = {
                'identificacion': form.cleaned_data['identificacion'],
                'tipo_id': form.cleaned_data['tipo_id']
            }

            deportista,tenant_existencia,existe = existencia_deportista(datos)

            if existe:
                datos = {
                    'identificacion': form.cleaned_data['identificacion'],
                    'tipo_id': form.cleaned_data['tipo_id'],
                    'nombre': deportista.nombres,
                    'apellido': deportista.apellidos,
                    'fecha_nacimiento': deportista.fecha_nacimiento.strftime("%Y-%m-%d")
                }
                request.session['datos'] = datos
                return redirect('preinscripcion_evento',id_evento)
            else:
                #Si no se encuentra el deportista entonces se redirecciona a registro de deportista con los datos iniciales en una sesión
                request.session['datos'] = datos
                return redirect('preinscripcion_evento',id_evento)

    else:
        form = VerificarExistenciaForm()
    return render(request,'deportistas/verificar_deportista.html',{'form':form,
                                                                   'existe':False})

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
                    noticia.foto = "clasificados/clasificados-default.png"
                elif nueva_foto != "si":
                    noticia.foto = nueva_foto

                if noticia.video:
                    noticia.video = noticia.video.replace("watch?v=", "embed/")

                noticia.previsualizacion = request.POST.get("previsualizacion")
                noticia.etiquetas = noticia.etiquetas.upper()
                form.save()

                messages.success(request, 'La noticia se ha editado correctamente')
                return redirect('listar_noticias')
    return render(request, 'registrar_evento.html', {'form': form,
                                               'edicion':True})


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

