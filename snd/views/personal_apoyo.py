from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from snd.formularios.personal_apoyo import PersonalApoyoForm, FormacionDeportivaForm, ExperienciaLaboralForm, VerificarExistenciaForm
from snd.models import PersonalApoyo, FormacionDeportiva, ExperienciaLaboral
from coldeportes.utilities import calculate_age,not_transferido_required
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from entidades.models import Entidad


@login_required
@permission_required('snd.add_personalapoyo')
def wizard_personal_apoyo_nuevo(request):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Crear un Personal de apoyo

    Si se envió un formulario a través del método POST, se hace el registro del personal de apoyo y se pasa a la siguiente fase del wizard
    de lo contrario se muestra la primera etapa con el formulario vacío sin guardar nada en la base de datos.

    :param request: Petición Realizada
    :type request:    WSGIRequest
    """

    try:
        datos = request.session['datos']
    except Exception:
        return redirect('verificar_personal_apoyo')

    personal_apoyo_form = PersonalApoyoForm(initial=datos)

    #personal_apoyo_form = PersonalApoyoForm()
    if request.method == 'POST':

        personal_apoyo_form = PersonalApoyoForm(request.POST, request.FILES)

        if personal_apoyo_form.is_valid():
            personal_apoyo = personal_apoyo_form.save(commit=False)
            personal_apoyo.entidad = request.tenant
            personal_apoyo.nombres = personal_apoyo.nombres.upper()
            personal_apoyo.apellidos = personal_apoyo.apellidos.upper()
            personal_apoyo.tipo_id = personal_apoyo.tipo_id.upper()
            personal_apoyo.save()
            personal_apoyo_form.save()
            return redirect('wizard_formacion_deportiva', personal_apoyo.id)

    return render(request, 'personal_apoyo/wizard/wizard_personal_apoyo.html', {
        'titulo': 'Información básica',
        'wizard_stage': 1,
        'form': personal_apoyo_form,
        'edicion':False
    })

@login_required
@permission_required('snd.add_personalapoyo')
def finalizar_personal_apoyo(request, opcion):
    """
    Junio 16 / 2015
    Autor: Milton Lenis

    enviar mensaje de finalizada la creación de personal de apoyo


    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param opcion: Opción para redireccionamiento
    :type opcion: String
    """
    messages.success(request, "Personal de apoyo registrado correctamente.")
    try:
        del request.session['datos']
    except:
        pass
    if opcion=='nuevo':
        return redirect('personal_apoyo_nuevo')
    elif opcion =='listar':
        return redirect('personal_apoyo_listar')


@login_required
@permission_required('snd.change_personalapoyo')
def wizard_personal_apoyo(request,id_personal_apoyo):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Editar un Personal de apoyo: Primer paso, información de identifiación del personal de apoyo

    Se obtiene el id del personal de apoyo, se busca, se verifica que se hayan realizado cambios y se almacenan los cambios realizados.

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_personal_apoyo: Llave primaria del personal de apoyo
    :type id_personal_apoyo: String
    """

    try:
        personal_apoyo = PersonalApoyo.objects.get(id=id_personal_apoyo)
    except Exception:
        personal_apoyo = None

    personal_apoyo_form = PersonalApoyoForm(instance=personal_apoyo)

    if request.method == 'POST':

        personal_apoyo_form = PersonalApoyoForm(request.POST, request.FILES, instance=personal_apoyo)

        if personal_apoyo_form.is_valid():
            personal_apoyo = personal_apoyo_form.save(commit=False)
            personal_apoyo.nombres = personal_apoyo.nombres.upper()
            personal_apoyo.apellidos = personal_apoyo.apellidos.upper()
            personal_apoyo.tipo_id = personal_apoyo.tipo_id.upper()
            personal_apoyo.save()
            personal_apoyo_form.save()
            return redirect('wizard_formacion_deportiva', id_personal_apoyo)
        print(personal_apoyo_form.errors)
    return render(request, 'personal_apoyo/wizard/wizard_personal_apoyo.html', {
        'titulo': 'Información básica',
        'wizard_stage': 1,
        'form': personal_apoyo_form,
        'id_personal_apoyo':personal_apoyo.id,
        'edicion':True
    })


@login_required
@permission_required('snd.change_personalapoyo')
def wizard_formacion_deportiva(request, id_personal_apoyo):
    """

    Junio 9 / 2015
    Autor: Milton Lenis

    Paso 2 del wizard: Datos de formación deportiva para un personal de apoyo

    Se obtiene la información de la peticion, se intenta buscar un objeto FormacionDeportiva para verificar si existe (se desea modificar)
    En caso de haber modificaciones se guardan.
    Si la informacion para la FormacionDeportiva del personal de apoyo es nueva se inicializa en nulo para que los formularios estén vacíos.

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_personal_apoyo: Llave primaria del personal de apoyo
    :type id_personal_apoyo: String
    """

    try:
        formacion_deportiva = FormacionDeportiva.objects.filter(personal_apoyo=id_personal_apoyo)
        edicion = True
    except Exception:
        formacion_deportiva = None
        edicion = False

    personal_apoyo= PersonalApoyo.objects.get(id=id_personal_apoyo)

    formaciondep_form = FormacionDeportivaForm()

    if request.method == 'POST':
        formaciondep_form = FormacionDeportivaForm(request.POST, request.FILES)
        if formaciondep_form.is_valid():
            formacion_deportiva = formaciondep_form.save(commit=False)
            formacion_deportiva.personal_apoyo = personal_apoyo
            formacion_deportiva.save()
            formaciondep_form.save()
            return redirect('wizard_formacion_deportiva', id_personal_apoyo)
        print(formaciondep_form.errors)

    return render(request, 'personal_apoyo/wizard/wizard_formacion_deportiva.html', {
        'titulo': 'Formación académica',
        'wizard_stage': 2,
        'form': formaciondep_form,
        'historicos': formacion_deportiva,
        'id_personal_apoyo': id_personal_apoyo,
        'edicion': edicion
    })

@login_required
@permission_required('snd.change_personalapoyo')
def eliminar_formacion_deportiva(request,id_personal_apoyo,id_formacion):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Eliminar un registro de formación deportiva

    Se obtiene el registro de la formación deportiva que se desea eliminar y se procede a eliminarlo de la base de datos.

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_personal_apoyo: Llave primaria del personal de apoyo
    :type id_personal_apoyo: String
    :param id_formacion: Llave primaria de la formación deportiva
    :type id_formacion: String
    """

    try:
        formacion_deportiva = FormacionDeportiva.objects.get(id=id_formacion, personal_apoyo=id_personal_apoyo)
        formacion_deportiva.delete()
        return redirect('wizard_formacion_deportiva', id_personal_apoyo)

    except Exception:
        return redirect('wizard_formacion_deportiva', id_personal_apoyo)


@login_required
@permission_required('snd.change_personalapoyo')
def wizard_experiencia_laboral(request, id_personal_apoyo):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Paso 3: Ingreso de la experiencia laboral de un personal de apoyo, en caso se haber experiencias laborales registradas, se muestran,
    en caso de ser una nueva experiencia laboral a registrar, se adiciona a la base de datos.
    Si no hay Experiencia laboral registrada se inicializa en nulo para que se muestren los formularios vacíos

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_personal_apoyo: Llave primaria del personal de apoyo
    :type id_personal_apoyo: String
    """

    try:
        experiencia_laboral = ExperienciaLaboral.objects.filter(personal_apoyo=id_personal_apoyo)
        edicion = True
    except Exception:
        experiencia_laboral = None
        edicion = False

    personal_apoyo = PersonalApoyo.objects.get(id=id_personal_apoyo)

    experiencia_laboral_form = ExperienciaLaboralForm()

    if request.method == 'POST':
        experiencia_laboral_form = ExperienciaLaboralForm(request.POST, request.FILES)

        if experiencia_laboral_form.is_valid():
            experiencia_laboral_nuevo = experiencia_laboral_form.save(commit=False)
            if experiencia_laboral_nuevo.actual:
                experiencia_laboral_nuevo.fecha_fin = None
            experiencia_laboral_nuevo.personal_apoyo = personal_apoyo
            experiencia_laboral_nuevo.nombre_cargo = experiencia_laboral_nuevo.nombre_cargo.upper()
            experiencia_laboral_nuevo.institucion = experiencia_laboral_nuevo.institucion.upper()
            experiencia_laboral_nuevo.save()
            experiencia_laboral_form.save()
            return redirect('wizard_experiencia_laboral', id_personal_apoyo)


    return render(request, 'personal_apoyo/wizard/wizard_experiencia_laboral.html', {
        'titulo': 'Información sobre la experiencia laboral',
        'wizard_stage': 3,
        'form': experiencia_laboral_form,
        'historicos': experiencia_laboral,
        'id_personal_apoyo': id_personal_apoyo,
        'edicion':edicion
    })

@login_required
@permission_required('snd.change_personalapoyo')
def eliminar_experiencia_laboral(request,id_personal_apoyo,id_experiencia):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Eliminar un registro de experiencia laboral

    Se obtiene el registro de la experiencia laboral que se desea eliminar y se procede a eliminarlo de la base de datos.

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_personal_apoyo: Llave primaria del personal de apoyo
    :type id_personal_apoyo: String
    :param id_experiencia: Llave primaria de la experiencia deportiva
    :type id_experiencia: String
    """

    try:
        experiencia_laboral = ExperienciaLaboral.objects.get(id=id_experiencia, personal_apoyo=id_personal_apoyo)
        experiencia_laboral.delete()
        return redirect('wizard_experiencia_laboral', id_personal_apoyo)

    except Exception:
        return redirect('wizard_experiencia_laboral', id_personal_apoyo)



@login_required
@permission_required('snd.change_personalapoyo')
def desactivar_personal_apoyo(request,id_personal_apoyo):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Cambiar estado de un personal de apoyo

    Se obtiene el estado actual y se invierte su valor

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_personal_apoyo: Llave primaria del personal de apoyo
    :type id_personal_apoyo: String
    """
    try:
        personal_apoyo = PersonalApoyo.objects.get(id=id_personal_apoyo)
    except:
        messages.error(request, "Error: Personal de apoyo no existe .")
        return redirect('personal_apoyo_listar')

    estado_actual = personal_apoyo.estado
    personal_apoyo.estado = not(estado_actual)
    personal_apoyo.save()
    if(estado_actual):
        message = "Personal de apoyo activado correctamente."
    else:
        message = "Personal de apoyo desactivado correctamente."
    messages.success(request, message)
    return redirect('personal_apoyo_listar')

@login_required
@permission_required('snd.view_personalapoyo')
def listar_personal_apoyo(request):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Listar personal de apoyo de un tenant

    Se obtienen los personales de apoyo y se listan

    :param request: Petición Realizada
    :type request: WSGIRequest
    """

    return render(request, 'personal_apoyo/personal_apoyo_lista.html', {
        'tipo_tenant':request.tenant.tipo
    })

@login_required
@permission_required('snd.view_personalapoyo')
def ver_personal_apoyo(request,id_personal_apoyo,id_entidad):
    """
    Junio 23 /2015
    Autor: Milton Lenis

    Ver Personal de apoyo

    Se obtiene la informacion general del personal de apoyo desde la base de datos y se muestra

    Edición: Septiembre 1 /2015
    NOTA: Para esta funcionalidad se empezó a pedir la entidad para conectarse y obtener la información de un objeto
    desde la entidad correcta, esto para efectos de consulta desde una liga o una federación.

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_personal_apoyo: Llave primaria del personal de apoyo
    :type id_personal_apoyo: String
    :param id_entidad: Llave primaria de la entidad a la que pertenece el personal de apoyo
    :type id_entidad: String
    """
    tenant = Entidad.objects.get(id=id_entidad).obtenerTenant()
    connection.set_tenant(tenant)
    ContentType.objects.clear_cache()
    try:
        personal_apoyo = PersonalApoyo.objects.get(id=id_personal_apoyo)
    except:
        messages.error(request, "Error: No existe el personal de apoyo solicitado o su información es incompleta")
        return redirect('personal_apoyo_listar')
    formacion_deportiva = FormacionDeportiva.objects.filter(personal_apoyo=personal_apoyo)
    experiencia_laboral = ExperienciaLaboral.objects.filter(personal_apoyo=personal_apoyo)
    personal_apoyo.edad = calculate_age(personal_apoyo.fecha_nacimiento)
    return render(request,'personal_apoyo/ver_personal_apoyo.html',{
            'personal_apoyo':personal_apoyo,
            'formacion_deportiva':formacion_deportiva,
            'experiencia_laboral':experiencia_laboral
        })

@login_required
@permission_required('snd.add_personalapoyo')
def verificar_personal_apoyo(request):
    """
    Julio 24 /2015
    Autor: Milton Lenis

    Verificación de la existencia de un personal de apoyo
    Se verifica si existe el personal de apoyo en la entidad actual, si existe en otra entidad o si no existe.
    Dependiendo del caso se muestra una respuesta diferente al usuario

    :param request: Petición Realizada
    :type request: WSGIRequest
    """

    if request.method=='POST':
        form = VerificarExistenciaForm(request.POST)
        if form.is_valid() and form.validar_id():
            datos = {
                'identificacion': form.cleaned_data['identificacion'],
                'tipo_id': form.cleaned_data['tipo_id']
            }

            #Verificación de existencia dentro del tenant actual
            try:
                personal_apoyo = PersonalApoyo.objects.get(identificacion=datos['identificacion'],tipo_id=datos['tipo_id'])
            except Exception:
                personal_apoyo = None

            if personal_apoyo:
                #Si se encuentra el personal_apoyo se carga el template con la existe=True para desplegar el aviso al usuario
                return render(request,'personal_apoyo/verificar_personal_apoyo.html',{'existe':True,
                                                                   'personal_apoyo':personal_apoyo})

            if not personal_apoyo:
                #Si no se encuentra en el tenant actual se debe verificar en otros tenants
                #Verificación de existencia en otros tenants
                #Estas dos variables son para ver si existe en otro tenant (True, False) y saber en cual Tenant se encontró
                existencia = False
                tenant_actual = connection.tenant
                tenant_existencia = None
                entidades = Entidad.objects.all()
                for entidad in entidades:
                    connection.set_tenant(entidad)
                    ContentType.objects.clear_cache()
                    try:
                        personal_apoyo = PersonalApoyo.objects.get(identificacion=datos['identificacion'],tipo_id=datos['tipo_id'])
                        existencia = True
                        tenant_existencia = entidad
                        break
                    except Exception:
                        pass

                connection.set_tenant(tenant_actual)

                if existencia:
                    return render(request,'personal_apoyo/verificar_personal_apoyo.html',{'existe':True,
                                                                                   'personal_apoyo':personal_apoyo,
                                                                                   'tenant_existencia':tenant_existencia})
                else:
                    #Si no se encuentra el personal_apoyo entonces se redirecciona a registro de personal de apoyo con los datos iniciales en una sesión
                    request.session['datos'] = datos
                    return redirect('personal_apoyo_nuevo')

    else:
        form = VerificarExistenciaForm()
    return render(request,'personal_apoyo/verificar_personal_apoyo.html',{'form':form,
                                                                    'existe':False})