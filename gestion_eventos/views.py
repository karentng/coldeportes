import binascii
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import *
from .models import Evento
from noticias.models import Noticia
from noticias.forms import NoticiaForm
from snd.formularios.deportistas import VerificarExistenciaForm
from snd.views.deportistas import existencia_deportista
import datetime


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


def editar_evento(request, id_evento):
    print("dsaddsd")
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        messages.error(request, 'El evento al que trata de acceder no existe!')
        return redirect('listar_eventos')

    form = EventoForm(instance=evento)

    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        nueva_foto = request.POST.get("imagen-crop")
        if form.has_changed or nueva_foto != "No":
            if form.is_valid():
                evento_form = form.save(commit=False)
                nueva_foto = request.POST.get('imagen-crop')

                if nueva_foto == "No":
                    evento_form.imagen = ""
                else:
                    evento_form.imagen = nueva_foto

                if evento_form.video:
                    evento_form.video = evento_form.video.replace("watch?v=", "embed/")
                evento_form.previsualizacion = request.POST.get("previsualizacion")
                evento_form.cupo_disponible = evento_form.cupo_participantes - evento.participantes.count()

                noticia_evento = evento.noticia
                noticia_evento.titulo = evento_form.titulo_evento
                noticia_evento.cuerpo_noticia = evento_form.descripcion_evento
                noticia_evento.fecha_expiracion = evento_form.fecha_finalizacion
                noticia_evento.autor = evento_form.autor
                noticia_evento.foto = evento_form.imagen
                noticia_evento.video = evento_form.video
                noticia_evento.etiquetas = ""
                noticia_evento.save()
                evento_form.save()

                messages.success(request, 'El evento se ha editado correctamente')
                return redirect('listar_eventos')

    return render(request, 'registrar_evento.html', {'form': form,
                                               'edicion':True})


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

    return render(request, 'listar_participantes.html', {'participantes': participantes, 'cupo': eventos.cupo_candidatos})


def preinscripcion_evento(request, id_evento):

    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        messages.error(request, 'El evento al que trata de acceder no existe!')
        return redirect('listar_eventos')
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

    try:
        datos = request.session["datos"]
    except Exception:
        return redirect('verificar_participante', id_evento)

    participante_form = ParticipanteForm(initial=datos)
    del request.session["datos"]
    return render(request, 'registrar_preinscrito.html', {'form': participante_form})


def editar_participante(request, id_participante):

    try:
        participante = Participante.objects.get(id=id_participante)
    except Exception:
        messages.error(request, 'El participante al que trata de acceder no existe!')
        return redirect('listar_eventos')

    if request.method == 'POST':
        participante_form = ParticipanteForm(request.POST, instance=participante)
        if participante_form.has_changed():
            if participante_form.is_valid():
                participante_form.save()

                messages.success(request, "El participante ha sido editado con exito!")
                return redirect('listar_participantes', participante.evento_participe)

    participante_form = ParticipanteForm(instance=participante)
    return render(request, 'registrar_preinscrito.html', {'form': participante_form, 'edicion': True})


def verificar_participante(request, id_evento):

    try:
        evento = Evento.objects.get(id=id_evento)
        hoy = datetime.date.today()
        if evento.fecha_inicio_preinscripcion > hoy:
            messages.error(request, 'El evento aún no se encuentra en etapa de preinscripcion')
            return redirect('listar_eventos')
        elif evento.fecha_finalizacion_preinscripcion < hoy:
            messages.error(request, 'La etapa de preinscripcion del evento ya finalizó')
            return redirect('listar_eventos')

        if evento.cupo_disponible == 0:
            messages.error(request, 'No hay cupos disponibles para el evento!')
            return redirect('listar_eventos')
    except Exception:
        messages.error(request, 'El evento al que trata de acceder no existe!')
        return redirect('listar_eventos')

    if request.method=='POST':
        form = VerificarExistenciaForm(request.POST)

        if form.is_valid():
            datos = {
                'identificacion': form.cleaned_data['identificacion'],
                'tipo_id': form.cleaned_data['tipo_id']
            }
            try:
                participante = evento.participantes.get(tipo_id=datos['tipo_id'],identificacion=datos['identificacion'])
                if participante:
                    messages.error(request, 'El participante ya se encuentra inscrito')
                    form = VerificarExistenciaForm()
                    return render(request,'deportistas/verificar_deportista.html',{'form':form,
                                                                   'existe':False})

            except Exception:
                pass
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
            messages.error(request, 'El evento al que trata de acceder no existe!')
            return render(request,'deportistas/verificar_deportista.html',{'form':form,
                                                                   'existe':False})

    else:
        form = VerificarExistenciaForm()
    return render(request,'deportistas/verificar_deportista.html',{'form':form,
                                                                   'existe':False})


def aceptar_candidato(request, id_participante):
    from django.core.mail import EmailMessage
    try:
        participante = Participante.objects.get(id=id_participante)
    except Exception:
        messages.error(request, 'El participante al que trata de acceder no existe!')
        return redirect('listar_eventos')

    evento = Evento.objects.get(id=participante.evento_participe)
    if evento.cupo_candidatos == 0:
        messages.error(request, 'No hay cupos disponible!')
        return redirect('listar_participantes', evento.id)


    token = binascii.hexlify(os.urandom(25))
    participante.token_email = token
    participante.estado = 2
    participante.save()


    evento.cupo_candidatos = evento.cupo_candidatos - 1
    evento.save()
    print(str(token))
    messages.success(request, 'Se ha enviado la peticion de confirmación')
    return redirect('listar_participantes', evento.id)


def confirmar_participacion(request, id_participante):
    try:
        participante = Participante.objects.get(id=id_participante)
    except Exception:
        messages.error(request, 'El participante al que trata de acceder no existe!')
        return redirect('listar_eventos')

    try:
        token = request.GET.get("token")
        if participante.token_email != token:
            messages.error(request, 'No está autorizado para ingresar!')
            return redirect('listar_eventos')

        aceptar = request.GET["acp"]
        if aceptar == '1':
            participante.estado = 3
            participante.save()
            messages.success(request, 'Has aceptado la inscripción satisfactoriamente')
            return redirect('listar_eventos')
        else:
            participante.estado = 4
            participante.save()
            evento = Evento.objects.get(id=participante.evento_participe)
            evento.cupo_candidatos = evento.cupo_candidatos + 1
            evento.save()
            messages.success(request, 'Has rechazado la inscripción satisfactoriamente')
            return redirect('listar_eventos')


    except Exception:
        messages.error(request, 'Ha ocurrido un error')
        return redirect('listar_eventos')


def gestion_pago(request, id_participante):
    try:
        participante = Participante.objects.get(id=id_participante)
    except Exception:
        messages.error(request, 'El participante al que trata de acceder no existe!')
        return redirect('listar_eventos')

    if request.method == "POST":
        estado_pago = request.POST.get("pago")
        print(estado_pago)
        if estado_pago == '0':
            participante.pago_registrado = False
        else:
            participante.pago_registrado = True
        participante.save()
        messages.success(request, 'Se ha registrado el estado del pago correctamente')
        return redirect('listar_participantes', participante.evento_participe)


    return redirect('listar_eventos')

def registrar_actividad(request, id_evento):

    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        messages.error(request, 'El evento al que trata de acceder no existe!')
        return redirect('listar_eventos')

    actividad_form = ActividadForm()

    if request.method == 'POST':
        actividad_form = ActividadForm(request.POST)
        if actividad_form.is_valid():
            actividad = actividad_form.save(commit=False)
            actividad.evento_perteneciente = evento.id
            actividad.save()
            evento.actividades.add(actividad)
            evento.save()
            messages.success(request, "La actividad ha sido creada con exito!")
            return redirect('registrar_actividad', id_evento)
    lista_actividades = evento.actividades.all()
    return render(request, 'gestion_actividades.html', {'form': actividad_form, 'lista_actividades': lista_actividades,
                                                        'evento': evento})


def editar_actividad(request, id_actividad):
    try:
        actividad = Actividad.objects.get(id=id_actividad)
    except Exception:
        messages.error(request, 'La actividad a la que trata de acceder no existe!')
        return redirect('listar_eventos')

    actividad_form = ActividadForm(instance=actividad)

    if request.method == "POST":
        actividad_form = ActividadForm(request.POST, instance=actividad)
        if actividad_form.has_changed():
            if actividad_form.is_valid():
                actividad = actividad_form.save(commit=False)
                actividad.save()
                messages.success(request, "La actividad ha sido editada con exito!")
                return redirect('registrar_actividad', actividad.evento_perteneciente)

    evento = Evento.objects.get(id=actividad.evento_perteneciente)
    lista_actividades = evento.actividades.all()
    return render(request, 'gestion_actividades.html', {'form': actividad_form, 'lista_actividades': lista_actividades,
                                                        'evento': evento, 'edicion': True})


def ver_actividades(request, id_evento):

    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        messages.error(request, 'El evento al que trata de acceder no existe!')
        return redirect('listar_eventos')

    actividades = evento.actividades.all()
    return render(request, 'ver_actividades.html', {'actividades': actividades,
                                                    'evento': evento})


def cambio_fecha_actividad(request):

    if request.is_ajax():
        response = {
            'status': 'error',
            'message': 'actividad no existe'
        }
        try:
            actividad = Actividad.objects.get(id=request.POST.get("id"))
        except Exception:
            return JsonResponse(response)

        dias = request.POST.get("delta_dias")
        mins = request.POST.get("delta_minutos")
        if not mins:
            actividad.dia_actividad = actividad.dia_actividad + datetime.timedelta(days=int(dias))
            actividad.save()
            message = "ok"
        else:
            try:
                actividad.hora_inicio = (datetime.datetime.combine(actividad.dia_actividad, actividad.hora_inicio) + datetime.timedelta(minutes=int(mins))).time()
                actividad.hora_fin = (datetime.datetime.combine(actividad.dia_actividad, actividad.hora_fin) + datetime.timedelta(minutes=int(mins))).time()
                actividad.dia_actividad = actividad.dia_actividad + datetime.timedelta(days=int(dias))
                actividad.save()
                message = "ok"
            except Exception as e:
                print(e)
                message = e
        response = {
            'status': 'ok',
            'message': message
        }
        return JsonResponse(response)

    return redirect('listar_eventos')

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

