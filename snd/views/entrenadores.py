from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from snd.formularios.entrenadores import EntrenadorForm, FormacionDeportivaForm, ExperienciaLaboralForm
from snd.models import Entrenador, FormacionDeportiva, ExperienciaLaboral


@login_required
def wizard_entrenador_nuevo(request):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Crear un Entrenador

    Si se envió un formulario a través del método POST, se hace el registro del entrenador y se pasa a la siguiente fase del wizard
    de lo contrario se muestra la primera etapa con el formulario vacío sin guardar nada en la base de datos.

    :param request: Petición Realizada
    :type request:    WSGIRequest
    """

    entrenador_form = EntrenadorForm()

    if request.method == 'POST':

        entrenador_form = EntrenadorForm(request.POST, request.FILES)

        if entrenador_form.is_valid():
            entrenador = entrenador_form.save(commit=False)
            entrenador.entidad_vinculacion = request.tenant
            entrenador.save()
            entrenador_form.save()
            return redirect('wizard_formacion_deportiva', entrenador.id)


    return render(request, 'entrenadores/wizard/wizard_entrenador.html', {
        'titulo': 'Información básica',
        'wizard_stage': 1,
        'form': entrenador_form,
    })



@login_required
def wizard_entrenador(request,id_entrenador):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Editar un Entrenador: Primer paso, información de identifiación del entrenador

    Se obtiene el id del entrenador, se busca, se verifica que se hayan realizado cambios y se almacenan los cambios realizados.

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_entrenador: Llave primaria del entrenador
    :type id_entrenador: String
    """

    try:
        entrenador = Entrenador.objects.get(id=id_entrenador)
    except Exception:
        entrenador = None

    entrenador_form = EntrenadorForm(instance=entrenador)

    if request.method == 'POST':

        entrenador_form = EntrenadorForm(request.POST, request.FILES, instance=entrenador)

        if entrenador_form.is_valid():
            entrenador_form.save()
            return redirect('wizard_formacion_deportiva', id_entrenador)


    return render(request, 'entrenadores/wizard/wizard_entrenador.html', {
        'titulo': 'Información básica',
        'wizard_stage': 1,
        'form': entrenador_form,
    })


@login_required
def wizard_formacion_deportiva(request,id_entrenador):
    """

    Junio 9 / 2015
    Autor: Milton Lenis

    Paso 2 del wizard: Datos de formación deportiva para un entrenador

    Se obtiene la información de la peticion, se intenta buscar un objeto FormacionDeportiva para verificar si existe (se desea modificar)
    En caso de haber modificaciones se guardan.
    Si la informacion para la FormacionDeportiva del entrenador es nueva se inicializa en nulo para que los formularios estén vacíos.

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_entrenador: Llave primaria del entrenador
    :type id_entrenador: String
    """

    try:
        formacion_deportiva = FormacionDeportiva.objects.filter(entrenador=id_entrenador)
    except Exception:
        formacion_deportiva = None

    formaciondep_form = FormacionDeportivaForm()

    if request.method == 'POST':
        formaciondep_form = FormacionDeportivaForm(request.POST)

        if formaciondep_form.is_valid():
            formacion_deportiva = formaciondep_form.save(commit=False)
            formacion_deportiva.entrenador = Entrenador.objects.get(id=id_entrenador)
            formacion_deportiva.save()
            formaciondep_form.save()
            return redirect('wizard_formacion_deportiva', id_entrenador)

    return render(request, 'entrenadores/wizard/wizard_formacion_deportiva.html', {
        'titulo': 'Información sobre la formación deportiva',
        'wizard_stage': 2,
        'form': formaciondep_form,
        'historicos': formacion_deportiva,
        'id_entrenador': id_entrenador
    })

@login_required
def eliminar_formacion_deportiva(request,id_entrenador,id_formacion):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Eliminar un registro de formación deportiva

    Se obtiene el registro de la formación deportiva que se desea eliminar y se procede a eliminarlo de la base de datos.

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_entrenador: Llave primaria del entrenador
    :type id_entrenador: String
    :param id_formacion: Llave primaria de la formación deportiva
    :type id_formacion: String
    """

    try:
        formacion_deportiva = FormacionDeportiva.objects.get(id=id_formacion, entrenador=id_entrenador)
        formacion_deportiva.delete()
        return redirect('wizard_formacion_deportiva', id_entrenador)

    except Exception:
        return redirect('wizard_formacion_deportiva', id_entrenador)


@login_required
def wizard_experiencia_laboral(request,id_entrenador):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Paso 3: Ingreso de la experiencia laboral de un entrenador, en caso se haber experiencias laborales registradas, se muestran,
    en caso de ser una nueva experiencia laboral a registrar, se adiciona a la base de datos.
    Si no hay Experiencia laboral registrada se inicializa en nulo para que se muestren los formularios vacíos

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_entrenador: Llave primaria del entrenador
    :type id_entrenador: String
    """

    try:
        experiencia_laboral = ExperienciaLaboral.objects.filter(entrenador=id_entrenador)
    except Exception:
        experiencia_laboral = None

    experiencia_laboral_form = ExperienciaLaboralForm()

    if request.method == 'POST':
        experiencia_laboral_form = ExperienciaLaboralForm(request.POST)

        if experiencia_laboral_form.is_valid():
            experiencia_laboral_nuevo = experiencia_laboral_form.save(commit=False)
            experiencia_laboral_nuevo.entrenador = Entrenador.objects.get(id=id_entrenador)
            experiencia_laboral_nuevo.save()
            experiencia_laboral_form.save()
            return redirect('wizard_experiencia_laboral', id_entrenador)


    return render(request, 'entrenadores/wizard/wizard_experiencia_laboral.html', {
        'titulo': 'Información sobre la experiencia laboral',
        'wizard_stage': 3,
        'form': experiencia_laboral_form,
        'historicos': experiencia_laboral,
        'id_entrenador': id_entrenador
    })

@login_required
def eliminar_experiencia_laboral(request,id_entrenador,id_experiencia):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Eliminar un registro de experiencia laboral

    Se obtiene el registro de la experiencia laboral que se desea eliminar y se procede a eliminarlo de la base de datos.

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_entrenador: Llave primaria del entrenador
    :type id_entrenador: String
    :param id_experiencia: Llave primaria de la experiencia deportiva
    :type id_experiencia: String
    """

    try:
        experiencia_laboral = ExperienciaLaboral.objects.get(id=id_experiencia, entrenador=id_entrenador)
        experiencia_laboral.delete()
        return redirect('wizard_experiencia_laboral', id_entrenador)

    except Exception:
        return redirect('wizard_experiencia_laboral', id_entrenador)



@login_required
def cambiar_estado_entrenador(request,id_entrenador):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Cambiar estado de un entrenador

    Se obtiene el estado actual y se invierte su valor

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_entrenador: Llave primaria del entrenador
    :type id_entrenador: String
    """
    entrenador = Entrenador.objects.get(id=id_entrenador)
    estado_actual = entrenador.activo
    entrenador.activo = not(estado_actual)
    entrenador.save()
    return redirect('entrenador_listar')

@login_required
def listar_entrenador(request):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Listar entrenadores de un tenant

    Se obtienen los entrenadores y se listan

    :param request: Petición Realizada
    :type request: WSGIRequest
    """

    entrenadores = Entrenador.objects.all()
    return render(request, 'entrenadores/entrenadores_lista.html', {
        'entrenadores':entrenadores,
    })