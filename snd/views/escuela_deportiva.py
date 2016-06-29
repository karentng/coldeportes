from django.db import connection
from snd.formularios.escuela_deportiva import *
from snd.models import *
from entidades.models import *
from django.contrib import messages
from coldeportes.utilities import *

import datetime


@login_required
@all_permission_required('snd.add_escueladeportiva')
def wizard_nuevo_sede(request):
    from django.db import IntegrityError

    escuela_form = EscuelaDeportivaForm()

    if request.method == 'POST':

        escuela_form = EscuelaDeportivaForm(request.POST)

        if escuela_form.is_valid():
            try:
                escuela = escuela_form.save(commit=False)
                escuela.entidad = request.tenant
                escuela.save()
                return redirect('wizard_servicios', escuela.id)

            except IntegrityError as e:
                if 'unique constraint' in str(e):
                    messages.error(request, "La sede que trata de registrar ya existe.")

    return render(request, 'escuela_deportiva/wizard/wizard_escuela_sede.html', {
        'titulo': 'Ingrese los datos de identificación y contacto de la sede de la Escuela de Formación Deportiva',
        'titulo_panel': 'Registro de Sede de EFD',
        'wizard_stage': 1,
        'form': escuela_form,
    })


@login_required
@all_permission_required('snd.add_escenario')
def wizard_sede(request, escuela_id):
    from django.db import IntegrityError
    try:
        escuela = EscuelaDeportiva.objects.get(id=escuela_id)
    except EscuelaDeportiva.DoesNotExist:
        messages.error(request, 'La sede a la que trata de acceder no existe')
        return redirect('wizard_nuevo_sede')

    escuela_form = EscuelaDeportivaForm(instance=escuela)

    if request.method == 'POST':

        escuela_form = EscuelaDeportivaForm(request.POST, instance=escuela)

        if escuela_form.is_valid():

            try:
                sede = escuela_form.save(commit=False)
                sede.entidad = request.tenant
                sede.save()
                return redirect('wizard_servicios', escuela.id)
            except IntegrityError as e:
                if 'unique constraint' in str(e):
                    messages.error(request, "La sede que trata de registrar ya existe.")

    return render(request, 'escuela_deportiva/wizard/wizard_escuela_sede.html', {
        'titulo': 'Ingrese los datos de identificación y contacto de la sede de la Escuela de Formación Deportiva',
        'titulo_panel': 'Edición de Sede de EFD',
        'wizard_stage': 1,
        'form': escuela_form,
        'escuela_id': escuela_id,
    })


@login_required
@all_permission_required('snd.add_escueladeportiva')
def wizard_servicios_sede(request, escuela_id):
    try:
        escuela = EscuelaDeportiva.objects.get(id=escuela_id)
    except EscuelaDeportiva.DoesNotExist:
        messages.error(request, 'La sede a la que trata de acceder no existe')
        return redirect('wizard_nuevo_sede')

    servicios_form = EscuelaDeportivaServiciosForm(instance=escuela)

    if request.method == 'POST':

        servicios_form = EscuelaDeportivaServiciosForm(request.POST, request.FILES, instance=escuela)

        if servicios_form.is_valid():
            escuela_servicios = servicios_form.save(commit=False)
            escuela_servicios.save()
            return redirect('wizard_horarios', escuela_id)

    return render(request, 'escuela_deportiva/wizard/wizard_servicios_sede.html', {
        'titulo': 'Seleccione los servicios que ofrece la sede de la Escuela de Formación Deportiva',
        'wizard_stage': 2,
        'titulo_panel': 'Registro de Servicios de Sede',
        'form': servicios_form,
        'escuela_id': escuela_id,
    })


@login_required
@all_permission_required('snd.add_escueladeportiva')
def wizard_horarios_sede(request, escuela_id):
    try:
        horarios = HorarioActividadesEscuela.objects.filter(sede=escuela_id)
    except Exception:
        horarios = None

    try:
        sede = EscuelaDeportiva.objects.get(id=escuela_id)
    except EscuelaDeportiva.DoesNotExist:
        messages.error(request, 'La sede a la que trata de acceder no existe')
        return redirect('wizard_nuevo_sede')

    horarios_form = HorarioActividadesEscuelaForm()

    if request.method == 'POST':
        horarios_form = HorarioActividadesEscuelaForm(request.POST)
        if horarios_form.is_valid():
            horario_nuevo = horarios_form.save(commit=False)
            horario_nuevo.sede = sede
            horario_nuevo.save()
            horarios_form.save_m2m()
            messages.success(request, "Horario registrado correctamente")
            return redirect('wizard_horarios_sede', escuela_id)
        else:
            print(horarios_form.errors)

    return render(request, 'escuela_deportiva/wizard/wizard_horarios_sede.html', {
        'titulo': 'Adicione los horarios de actividades de la sede de la EFD',
        'wizard_stage': 3,
        'titulo_panel': 'Registro de Horarios de Sede',
        'form': horarios_form,
        'horarios': horarios,
        'escuela_id': escuela_id,
    })


@login_required
@all_permission_required('snd.add_escueladeportiva')
def wizard_categorias_sede(request, escuela_id):
    try:
        categorias = CategoriaEscuela.objects.filter(sede=escuela_id)
    except Exception:
        categorias = None

    try:
        sede = EscuelaDeportiva.objects.get(id=escuela_id)
    except EscuelaDeportiva.DoesNotExist:
        messages.error(request, 'La sede a la que trata de acceder no existe')
        return redirect('wizard_nuevo_sede')

    categorias_form = CategoriaEscuelaForm()

    if request.method == 'POST':
        categorias_form = CategoriaEscuelaForm(request.POST)
        if categorias_form.is_valid():
            cateforia_nueva = categorias_form.save(commit=False)
            cateforia_nueva.sede = sede
            cateforia_nueva.save()
            messages.success(request, "Categoría registrada correctamente")
            return redirect('wizard_categorias_sede', escuela_id)
        else:
            print(categorias.errors)

    return render(request, 'escuela_deportiva/wizard/wizard_categorias_sede.html', {
        'titulo': 'Adicione las categorías de la sede de la EFD',
        'wizard_stage': 4,
        'titulo_panel': 'Registro de Categorías de Sede',
        'form': categorias_form,
        'categorias': categorias,
        'escuela_id': escuela_id,
    })


@login_required
@all_permission_required('snd.add_escueladeportiva')
def eliminar_horario_sede(request, escuela_id, horario_id):
    try:
        horario = HorarioActividadesEscuela.objects.get(id=horario_id, sede=escuela_id)
        horario.delete()
        messages.success(request, "Horario eliminado correctamente")
        return redirect('wizard_horarios_sede', escuela_id)

    except Exception as e:
        return redirect('wizard_horarios_sede', escuela_id)


@login_required
@all_permission_required('snd.add_escueladeportiva')
def eliminar_categoria_sede(request, escuela_id, categoria_id):
    try:
        categorias = CategoriaEscuela.objects.filter(sede=escuela_id)
        if categorias.count() == 1:
            messages.error(request, "La sede debe tener almenos 1 categoría")
            return redirect('wizard_categorias_sede', escuela_id)

        categoria = categorias.get(id=categoria_id)
        participantes = Participante.objects.filter(categoria=categoria)
        if participantes.count() > 0:
            messages.error(request, "Hay participantes inscritos en esta categoría")
            return redirect('wizard_categorias_sede', escuela_id)

        categoria.delete()
        messages.success(request, "Categoría eliminada correctamente")
        return redirect('wizard_categorias_sede', escuela_id)

    except Exception as e:
        return redirect('wizard_categorias_sede', escuela_id)


@login_required
@all_permission_required('snd.add_escueladeportiva')
def finalizar(request, escuela_id, opcion):

    categorias = CategoriaEscuela.objects.filter(sede=escuela_id)
    if categorias.count() == 0:
        messages.error(request, "La sede debe tener almenos 1 categoría")
        return redirect('wizard_categorias_sede', escuela_id)

    messages.success(request, "Sede de EFD registrada correctamente.")

    if opcion == "nuevo":
        return redirect('wizard_nuevo_sede')
    else:
        return redirect('escuela_deportiva_listar')


@login_required
@all_permission_required('snd.view_escueladeportiva')
def ver(request, escuela_deportiva_id, id_entidad):
    """
    Noviembre 02 / 2015
    Autor: Cristian Leonardo Ríos López
    
    ver escuela de formación deportiva

    Se obtienen toda la información registrada de la escual de formación deportiva dada y se muestra.

    Se pide la entidad para conectarse y obtener la información de un objeto
    desde la entidad correcta, esto para efectos de consulta desde otro ente cuando sea necesario.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escuela_deportiva_id:   Identificador de la escuela de formación deportiva
    :type escuela_deportiva_id:    String
    :param id_entidad: Llave primaria de la entidad a la que pertenece la escuela de formación deportiva
    :type id_entidad: String
    """
    tenant = Entidad.objects.get(id=id_entidad).obtenerTenant()
    connection.set_tenant(tenant)
    ContentType.objects.clear_cache()
    try:
        escuela_deportiva = EscuelaDeportiva.objects.get(id=escuela_deportiva_id)
        horarios = HorarioActividadesEscuela.objects.filter(sede=escuela_deportiva.id)
        categorias = CategoriaEscuela.objects.filter(sede=escuela_deportiva_id)
    except EscuelaDeportiva.DoesNotExist:
        messages.error(request, 'La escuela deportiva que desea ver no existe')
        return redirect('escuela_deportiva_listar')

    return render(request, 'escuela_deportiva/escuela_deportiva_ver.html', {
        'escuela': escuela_deportiva,
        'horarios': horarios,
        'categorias': categorias
    })


@login_required
@all_permission_required('snd.view_escueladeportiva')
def listar(request):
    """
    Noviembre 02 / 2015
    Autor: Cristian Leonardo Ríos López
    
    listar las escuelas de formación deportiva de la respectiva entidad

    Se pasa el tipo de tenant para que se haga la carga respectiva de datos

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    return render(request, 'escuela_deportiva/escuela_deportiva_lista.html', {
        'tipo_tenant': request.tenant.tipo
    })


@login_required
@permission_required('snd.change_escueladeportiva')
def desactivar_escuela_deportiva(request,id_escuela):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Cambiar estado de una escuela deportiva

    Se obtiene el estado actual y se invierte su valor

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_escuela: Llave primaria de la escuela
    :type id_escuela: String
    """
    try:
        escuela = EscuelaDeportiva.objects.get(id=id_escuela)
    except:
        messages.error(request, "La escuela que está intentando desactivar no existe")
        return redirect('escuela_deportiva_listar')

    estado_actual = escuela.estado
    escuela.estado = not estado_actual
    escuela.save()
    if estado_actual:
        message = "Escuela deportiva activada correctamente."
    else:
        message = "Escuela deportiva desactivada correctamente."
    messages.success(request, message)
    return redirect('escuela_deportiva_listar')


@login_required
@permission_required('snd.add_escueladeportiva')
def registrar_participante(request):

    if request.method == 'POST':
        sede_id = int(request.POST["sede_perteneciente"])
        participante_form = ParticipanteForm(request.POST, sede_id=sede_id)
        print(participante_form.fields['categoria'].__dict__)
        if participante_form.is_valid():
            participante = participante_form.save(commit=False)
            participante.entidad = request.tenant
            participante.save()
            messages.success(request, "El participante ha sido registrado con exito")
            return redirect('listar_participante')
        else:
            messages.error(request, "Error")
            return render(request, 'escuela_deportiva/registrar_participante.html', {'form': participante_form})

    participante_form = ParticipanteForm()
    return render(request, 'escuela_deportiva/registrar_participante.html', {'form': participante_form})


@login_required
@permission_required('snd.change_escueladeportiva')
def editar_participante(request, id_participante):
    try:
        participante = Participante.objects.get(id=id_participante)
    except Participante.DoesNotExist:
        messages.error(request, 'El participante al que trata de acceder no existe')
        return redirect("listar_participante")

    if request.method == 'POST':
        participante_form = ParticipanteForm(request.POST, request.FILES, instance=participante,
                                             sede_id=participante.sede_perteneciente.id)
        if participante_form.has_changed():
            if participante_form.is_valid():
                participante_form.save()
                messages.success(request, "El participante ha sido editado con exito")
                return redirect('listar_participante')
            else:
                print(participante_form.errors)
    participante_form = ParticipanteForm(instance=participante, sede_id=participante.sede_perteneciente.id)
    return render(request, 'escuela_deportiva/registrar_participante.html', {'form': participante_form,
                                                                             'edicion': True})


@login_required
@permission_required('snd.view_escueladeportiva')
def listar_participante(request):
    participantes = Participante.objects.all()
    return render(request, 'escuela_deportiva/listar_participantes.html', {'participantes': participantes})


@login_required
@permission_required('snd.view_escueladeportiva')
def detalles_participante(request, id_participante):
    try:
        participante = Participante.objects.get(id=id_participante)
        alertas = AlertaTemprana.objects.filter(participante=participante)
        alerta_form = AlertaTempranaForm()
        seguimientotyp_form = SeguimientoTallaPesoForm()
        seguimientostyp = SeguimientoTallaPeso.objects.filter(participante=participante)
    except Participante.DoesNotExist:
        messages.error(request, 'El participante al que trata de acceder no existe')
        return redirect("listar_participante")

    try:
        acudiente = Acudiente.objects.get(participante_responsable=participante.id)
    except Acudiente.DoesNotExist:
        acudiente = None
    return render(request, 'escuela_deportiva/ver_participante.html', {'participante': participante,
                                                                       'acudiente': acudiente, 'alertas': alertas,
                                                                       'alerta_form': alerta_form,
                                                                       'seguimientostyp': seguimientostyp,
                                                                       'seguimientotyp_form': seguimientotyp_form})


@login_required
@permission_required('snd.change_escueladeportiva')
def cambiar_estado_participante(request, id_participante):
    try:
        participante = Participante.objects.get(id=id_participante)
    except Participante.DoesNotExist:
        messages.error(request, 'El participante al que trata de acceder no existe')
        return redirect("listar_participante")

    participante.estado = not participante.estado
    participante.save()

    messages.success(request, "Participante "+participante.get_estado_accion()+" correctamente")
    return redirect('listar_participante')


@login_required
@permission_required('snd.change_escueladeportiva')
def gestion_alertas(request, id_participante):
    try:
        participante = Participante.objects.get(id=id_participante)
    except Participante.DoesNotExist:
        messages.error(request, 'El participante al que trata de acceder no existe')
        return redirect("listar_participante")

    if request.method == "POST":
        try:
            alerta_editar = AlertaTemprana.objects.get(id=int(request.POST["alerta_id"]))
        except AlertaTemprana.DoesNotExist:
            alerta_editar = None
        alerta_form = AlertaTempranaForm(request.POST, instance=alerta_editar)
        if alerta_form.is_valid():
            alerta = alerta_form.save(commit=False)
            alerta.participante = participante
            alerta.save()
            messages.success(request, 'Alerta registrada con éxito')
            return redirect("detalles_participante", id_participante)
        else:
            print(alerta_form.errors)

    return redirect("detalles_participante", id_participante)


@login_required
@permission_required('snd.change_escueladeportiva')
def cambiar_estado_alerta(request, id_alerta):
    try:
        alerta = AlertaTemprana.objects.get(id=id_alerta)
    except Participante.DoesNotExist:
        messages.error(request, 'La alerta a la que trata de acceder no existe')
        return redirect("listar_participante")

    alerta.estado = not alerta.estado
    alerta.fecha_ultima_actualizacion = datetime.datetime.now()
    alerta.save()

    messages.success(request, "Alerta "+alerta.get_estado_accion()+" correctamente")
    return redirect("detalles_participante", alerta.participante.id)


@login_required
@permission_required('snd.add_escueladeportiva')
def registrar_typ(request, id_participante):
    try:
        participante = Participante.objects.get(id=id_participante)
    except Participante.DoesNotExist:
        messages.error(request, 'El participante al que trata de acceder no existe')
        return redirect("listar_participante")

    if request.method == 'POST':
        seguimientotyp_form = SeguimientoTallaPesoForm(request.POST)
        if seguimientotyp_form.is_valid():
            seguimientotyp = seguimientotyp_form.save(commit=False)
            seguimientotyp.participante = participante
            seguimientotyp.save()
            participante.talla = seguimientotyp.talla
            participante.peso = seguimientotyp.peso
            participante.save()
            messages.success(request, "El seguimiento ha sido registrado con exito")
            return redirect("detalles_participante", id_participante)

    return redirect("detalles_participante", id_participante)


@login_required
@permission_required('snd.change_escueladeportiva')
def eliminar_typ(request, id_typ):
    try:
        seguimientotyp = SeguimientoTallaPeso.objects.get(id=id_typ)
    except Participante.DoesNotExist:
        messages.error(request, 'El seguimiento al que trata de acceder no existe')
        return redirect("listar_participante")

    id_participante = seguimientotyp.participante.id
    seguimientotyp.delete()

    messages.success(request, "El seguimiento ha sido eliminado con exito")
    return redirect("detalles_participante", id_participante)


@login_required
@permission_required('snd.change_escueladeportiva')
def ajax_alerta(request):
    from django.http import JsonResponse
    from django.template.loader import render_to_string
    if request.is_ajax():
        alerta_id = int(request.GET["alerta_id"])
        alerta = AlertaTemprana.objects.get(id=alerta_id)
        alerta_form = AlertaTempranaForm(instance=alerta)
        alerta_html = render_to_string("escuela_deportiva/alerta_editar.html",
                                       {"alerta_form": alerta_form, "participante_id": alerta.participante.id,
                                        "alerta_id": alerta.id})
        return JsonResponse({"html": alerta_html})

    return JsonResponse({"status": "error"})


@login_required
@permission_required('snd.add_escueladeportiva')
def ajax_categoria_sede(request):
    from django.http import JsonResponse
    if request.is_ajax():
        sede_id = int(request.GET["sede_id"])
        categorias = CategoriaEscuela.objects.filter(sede=sede_id)
        if categorias.count() == 0:
            return JsonResponse({"status": "empty"})
        else:
            data = []
            for categoria in categorias.all():
                dic = {}
                dic["id"] = categoria.id
                dic["text"] = categoria.nombre_categoria
                data.append(dic)
        return JsonResponse({"data": data})

    return JsonResponse({"status": "error"})


@login_required
@permission_required('snd.add_escueladeportiva')
def registrar_acudiente(request, id_participante):

    if request.method == 'POST':
        try:
            participante = Participante.objects.get(id=id_participante)
        except Participante.DoesNotExist:
            messages.error(request, 'El participante al que trata de acceder no existe')
            return redirect("listar_participante")
        acudiente_form = AcudienteForm(request.POST, request.FILES)
        if acudiente_form.is_valid():
            acudiente = acudiente_form.save(commit=False)
            acudiente.participante_responsable = participante
            acudiente.save()
            messages.success(request, "El acudiente ha sido registrado con exito")
            return redirect('detalles_participante', id_participante)

    acudiente_form = AcudienteForm()
    participantes_sin_acudiente = Participante.objects.exclude(id__in=(
        Acudiente.objects.all().values_list('participante_responsable', flat=True)
    ))
    acudiente_form.fields["participante_responsable"].queryset = participantes_sin_acudiente
    return render(request, 'escuela_deportiva/registrar_acudiente.html', {'form': acudiente_form})


@login_required
@permission_required('snd.change_escueladeportiva')
def editar_acudiente(request, id_acudiente):
    try:
        acudiente = Acudiente.objects.get(id=id_acudiente)
    except Acudiente.DoesNotExist:
        messages.error(request, 'El acudiente al que trata de acceder no existe')
        return redirect("listar_acudientes")

    if request.method == 'POST':
        acudiente_form = AcudienteForm(request.POST, request.FILES, instance=acudiente)
        if acudiente_form.has_changed():
            if acudiente_form.is_valid():
                acudiente_form.save()
                messages.success(request, "El acudiente ha sido editado con éxito")
                return redirect('listar_acudientes')

    acudiente_form = AcudienteForm(instance=acudiente)
    return render(request, 'escuela_deportiva/registrar_acudiente.html', {'form': acudiente_form,
                                                                          'edicion': True})


@login_required
@permission_required('snd.view_escueladeportiva')
def listar_acudientes(request):
    acudientes = Acudiente.objects.all()
    return render(request, 'escuela_deportiva/listar_acudientes.html', {'acudientes': acudientes})


@login_required
@permission_required('snd.change_escueladeportiva')
def cambiar_estado_acudiente(request, id_acudiente):
    try:
        acudiente = Acudiente.objects.get(id=id_acudiente)
    except Acudiente.DoesNotExist:
        messages.error(request, 'El acudiente al que trata de acceder no existe')
        return redirect("listar_acudientes")

    acudiente.estado = not acudiente.estado
    acudiente.save()

    messages.success(request, "Acudiente "+acudiente.get_estado_accion()+" correctamente")
    return redirect('listar_acudientes')


@login_required
@permission_required('snd.add_escueladeportiva')
def registrar_actividadefd(request):

    actividad_form = ActividadEFDForm()

    if request.method == 'POST':
        actividad_form = ActividadEFDForm(request.POST)
        if actividad_form.is_valid():
            actividad_form.save()
            messages.success(request, "La actividad ha sido creada con exito!")
            return redirect('registrar_actividadefd')
    return render(request, 'escuela_deportiva/registrar_actividad.html', {'form': actividad_form})


@login_required
@permission_required('snd.change_escueladeportiva')
def editar_actividadefd(request, id_actividad):
    try:
        actividad = ActividadEFD.objects.get(id=id_actividad)
        if actividad.estado == 0:
            messages.error(request, 'La actividad a la que trata de acceder se encuentra inactiva')
            return redirect('listar_actividadesefd')
    except Exception:
        messages.error(request, 'La actividad a la que trata de acceder no existe!')
        return redirect('listar_actividadesefd')

    actividad_form = ActividadEFDForm(instance=actividad)

    if request.method == "POST":
        actividad_form = ActividadEFDForm(request.POST, instance=actividad)
        if actividad_form.has_changed():
            if actividad_form.is_valid():
                actividad_form.save()
                messages.success(request, "La actividad ha sido editada con éxito!")
                return redirect('listar_actividadesefd')
        else:
            messages.success(request, "La actividad ha sido editada con éxito!")
            return redirect('listar_actividadesefd')

    return render(request, 'escuela_deportiva/registrar_actividad.html', {'form': actividad_form, 'edicion': True})


@login_required
@permission_required('snd.view_escueladeportiva')
def listar_actividadesefd(request):
    actividades = ActividadEFD.objects.all()
    return render(request, 'escuela_deportiva/listar_actividades.html', {'actividades': actividades})


@login_required
@permission_required('snd.change_escueladeportiva')
def cambiar_estado_actividadefd(request, id_actividad):
    try:
        actividad = ActividadEFD.objects.get(id=id_actividad)
    except ActividadEFD.DoesNotExist:
        messages.error(request, 'La actividad a la que trata de acceder no existe')
        return redirect("listar_actividadesefd")

    actividad.estado = not actividad.estado
    actividad.save()

    messages.success(request, "Actividad "+actividad.get_estado_accion()+" correctamente")
    return redirect('listar_actividadesefd')


@login_required
@permission_required('snd.view_escueladeportiva')
def listado_asistencia_actividad(request, id_actividad):
    try:
        actividad = ActividadEFD.objects.get(id=id_actividad)
    except Exception:
        messages.error(request, 'La actividad a la que trata de acceder no existe!')
        return redirect('listar_actividadesefd')

    if actividad.dirigido_a == 0:
        asistentes = Acudiente.objects.filter(participante_responsable__sede_perteneciente=actividad.sede).all()
        for asistente in asistentes:
            if asistente in actividad.acudientes.all():
                asistente.asistio = True
            else:
                asistente.asistio = False
    else:
        asistentes = Participante.objects.filter(sede_perteneciente=actividad.sede).all()
        for asistente in asistentes:
            if asistente in actividad.participantes.all():
                asistente.asistio = True
            else:
                asistente.asistio = False
    return render(request, 'escuela_deportiva/registrar_asistencia_actividad.html',
                  {'asistentes': asistentes, 'actividad': actividad})


@login_required
@permission_required('snd.add_escueladeportiva')
def ajax_asistencia(request):
    from django.http import JsonResponse
    if request.is_ajax():
        try:
            actividad_id = int(request.POST["actividad_id"])
            asistente_id = int(request.POST["asistente_id"])
            dirigido_a = int(request.POST["dirigido_a"])
            asistio = int(request.POST["asistio"])

            actividadefd = ActividadEFD.objects.get(id=actividad_id)

            if dirigido_a == 0:
                asistente = Acudiente.objects.get(id=asistente_id)
                if asistio:
                    actividadefd.acudientes.add(asistente)
                else:
                    actividadefd.acudientes.remove(asistente)
            else:
                asistente = Participante.objects.get(id=asistente_id)
                if asistio:
                    actividadefd.participantes.add(asistente)
                else:
                    actividadefd.participantes.remove(asistente)
        except Exception as e:
            return JsonResponse({"status": "error", "msj": "Ocurrió un error en el servidor"})

        return JsonResponse({"status": "ok", "msj": "Asistencia registrada correctamente"})

    return JsonResponse({"status": "error"})
