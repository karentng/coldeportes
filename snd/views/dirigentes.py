from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.contrib import messages
from formtools.wizard.views import *
from snd.formularios.dirigentes import *
from coldeportes.utilities import *
import json
from entidades.models import Entidad

@login_required
@all_permission_required('snd.add_dirigente')
def wizard_identificacion_nuevo(request):
    """
    Junio 14 / 2015
    Autor: Cristian Leonardo Ríos López
    
    Crear un Dirigente

    Se obtienen los formularios de información del dirigente con los datos diligenciados y se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """

    #print(request.session)
    try:
        datos = request.session['datos']
    except Exception:
        return redirect('dirigentes_verificar')

    identificacion_form = DirigenteForm(initial=datos)

    if request.method == 'POST':

        identificacion_form = DirigenteForm(request.POST, request.FILES)

        if identificacion_form.is_valid():
            dirigente = identificacion_form.save(commit=False)
            dirigente.entidad =  request.tenant
            dirigente.save()
            identificacion_form.save_m2m()
            del request.session['datos']
            return redirect('dirigentes_cargos', dirigente_id=dirigente.id, edicion=0)

    return render(request, 'dirigentes/wizard/wizard_identificacion.html', {
        'wizard_stage': 1,
        'form': identificacion_form,
        'edicion': 0
    })

@login_required
@all_permission_required('snd.add_dirigente')
def wizard_identificacion(request, dirigente_id):
    """
    Junio 14 / 2015
    Autor: Cristian Leonardo Ríos López
    
    Editar un Dirigente: Paso datos de identificación dirigente

    Se obtienen los formularios de información del dirigente con los datos diligenciados y se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param dirigente_id:   Identificador del dirigente
    :type dirigente_id:    String
    """

    try:
        dirigente = Dirigente.objects.get(id=dirigente_id)
    except Dirigente.DoesNotExist:
        messages.error(request, "Está tratando de editar un dirigente inexistente.")
        return redirect('dirigentes_listar')

    identificacion_form = DirigenteForm(instance=dirigente)

    if request.method == 'POST':

        identificacion_form = DirigenteForm(request.POST, request.FILES, instance=dirigente)

        if identificacion_form.is_valid():
            dirigente = identificacion_form.save(commit=False)
            dirigente.save()
            identificacion_form.save_m2m()
            return redirect('dirigentes_cargos', dirigente_id=dirigente_id, edicion=1)

    return render(request, 'dirigentes/wizard/wizard_identificacion.html', {
        'wizard_stage': 1,
        'form': identificacion_form,
        'edicion': 1,
        'dirigente_id': dirigente_id
    })


@login_required
@all_permission_required('snd.add_dirigente')
def wizard_cargos(request, dirigente_id, edicion):
    """
    Agosto 05 / 2015
    Autor: Cristian Leonardo Ríos López
    
    Cargos de un dirigente

    Se obtiene el formulario de los cargos del dirigente y se muestran los cargos actualmente añadido
    y si hay modificaciones se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param dirigente_id:   Identificador del dirigente
    :type dirigente_id:    String
    """

    cargos = DirigenteCargo.objects.filter(dirigente=dirigente_id)
    cargos_form = DirigenteCargosForm(dirigente_id=dirigente_id)

    if request.method == 'POST':
        cargos_form = DirigenteCargosForm(request.POST)

        if cargos_form.is_valid():
            cargo_nuevo = cargos_form.save(commit=False)
            try:
                cargo_nuevo.dirigente = Dirigente.objects.get(id=dirigente_id)
            except Dirigente.DoesNotExist:
                messages.error(request, "Está tratando de adicionarle cargos a un dirigente inexistente.")
                return redirect('dirigentes_listar')
            cargo_nuevo.save()
            return redirect('dirigentes_cargos', dirigente_id=dirigente_id, edicion=edicion)
                

    return render(request, 'dirigentes/wizard/wizard_cargos.html', {
        'wizard_stage': 2,
        'form': cargos_form,
        'cargos': cargos,
        'dirigente_id': dirigente_id,
        'edicion': edicion
        })

@login_required
@all_permission_required('snd.add_dirigente')
def cargos_ajax(request):
    """
    Agosto 09 / 2015
    Autor: Cristian Leonardo Ríos López
    
    Cargos de un dirigente

    Función Ajax. Se obtienen las funciones del cargo del dirigente.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param dirigente_id:   Identificador del dirigente
    :type dirigente_id:    String
    """
    if request.is_ajax():
        cargos = DirigenteCargo.objects.filter(dirigente=request.GET['dirigente_id'])
        cargos_ = []
        for cargo in cargos:
            cargos_.append({'value':cargo.id, 'text':cargo.__str__()})
        return HttpResponse(json.dumps({'cargos': cargos_}), content_type="application/json")
    else:
        raise Http404

@login_required
@all_permission_required('snd.add_dirigente')
def eliminar_cargo(request, cargo_id, dirigente_id):
    """
    Agosto 05 / 2015
    Autor: Cristian Leonardo Ríos López
    
    Eliminar cargo

    Se obtienen el cargo del dirigente de la base de datos y se elimina

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param dirigente_id   Identificador del dirigente
    :type dirigente_id    String
    :param cargo_id   Identificador del cargo del dirigente
    :type cargo_id    String
    """

    try:
        cargo = DirigenteCargo.objects.get(id=cargo_id, dirigente_id = dirigente_id)
        cargo.delete()
        messages.success(request,'El cargo ha sido eliminado con éxito.')
        return redirect('dirigentes_cargos',dirigente_id=dirigente_id, edicion=1)

    except DirigenteCargo.DoesNotExist:
        messages.error(request,'Está tratando de eliminar un cargo inexistente.')
        return redirect('dirigentes_cargos', dirigente_id=dirigente_id, edicion=1)


@login_required
@all_permission_required('snd.add_dirigente')
def wizard_funciones(request, dirigente_id, cargo_id=None, edicion=0):
    """
    Junio 14 / 2015
    Autor: Cristian Leonardo Ríos López
    
    Funciones del cargo de un dirigente

    Se obtienen el formulario de las funciones del cargo y se muestran las funciones actualmente añadidas al dirigente según el cargo
    y si hay modificaciones se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param cargo_id:   Identificador del cargo del dirigente
    :type cargo_id:    String
    :param dirigente_id:   Identificador del dirigente
    :type dirigente_id:    String
    """

    funciones_form = DirigenteFuncionesForm(dirigente_id=dirigente_id, cargo_id=cargo_id)

    if request.method == 'POST':
        funciones_form = DirigenteFuncionesForm(request.POST)

        if funciones_form.is_valid():
            funcion_nueva = funciones_form.save(commit=False)
            try:
                funcion_nueva.dirigente = Dirigente.objects.get(id=dirigente_id)
            except Dirigente.DoesNotExist:
                messages.error(request, "Está tratando de adicionarle funciones a un dirigente inexistente.")
                return redirect('dirigentes_listar')
            funcion_nueva.save()
            return redirect('dirigentes_funciones', dirigente_id, funcion_nueva.cargo.id, edicion)

    return render(request, 'dirigentes/wizard/wizard_funciones.html', {
        'wizard_stage': 3,
        'form': funciones_form,
        'dirigente_id': dirigente_id,
        'edicion': edicion
    })

@login_required
@all_permission_required('snd.add_dirigente')
def funciones_ajax(request):
    """
    Agosto 09 / 2015
    Autor: Cristian Leonardo Ríos López
    
    Funciones del cargo de un dirigente

    Función Ajax. Se obtienen las funciones del cargo del dirigente.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param cargo_id:   Identificador del cargo del dirigente
    :type cargo_id:    String
    :param dirigente_id:   Identificador del dirigente
    :type dirigente_id:    String
    """
    if request.is_ajax():
        funciones = DirigenteFuncion.objects.filter(dirigente=request.GET['dirigente_id'], cargo=request.GET['cargo_id'])
        funciones_ = []
        for funcion in funciones:
            funciones_.append({'id':funcion.id, 'descripcion':funcion.descripcion})
        return HttpResponse(json.dumps({'funciones': funciones_}), content_type="application/json")
    else:
        raise Http404

@login_required
@all_permission_required('snd.add_dirigente')
def eliminar_funcion(request, dirigente_id, cargo_id, funcion_id):
    """
    Junio 14 / 2015
    Autor: Cristian Leonardo Ríos López

    Eliminar función

    Se obtienen la función de la base de datos y se elimina

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param cargo_id   Identificador del cargo del dirigente
    :type cargo_id    String
    :param funcion_id   Identificador de la función
    :type funcion_id    String
    """

    try:
        funcion = DirigenteFuncion.objects.get(id=funcion_id, cargo=cargo_id, dirigente=dirigente_id)
        funcion.delete()
        messages.success(request,'La función ha sido eliminada con éxito.')
        return redirect('dirigentes_funciones', dirigente_id, cargo_id)

    except DirigenteFuncion.DoesNotExist:
        messages.error(request,'Está tratando de eliminar un función inexistente.')
        return redirect('dirigentes_funciones', dirigente_id, cargo_id)

@login_required
@all_permission_required('snd.add_dirigente')
def wizard_formacion_academica(request,dirigente_id, edicion):
    """
    Mayo 05 / 2016
    Autor: Daniel Correa

    Formacion academica de un dirigente

    Se obtiene el formulario de la formacion academica del dirigente y se muestra el historial actualmente añadido
    y si hay nuevos registros se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param dirigente_id:   Identificador del dirigente
    :type dirigente_id:    String
    """

    info_acad = DirigenteFormacionAcademica.objects.filter(dirigente=dirigente_id)

    try:
        dirigente = Dirigente.objects.get(id=dirigente_id)
    except:
        messages.error(request,'Está tratando de editar un dirigente inexistente.')
        return redirect('dirigentes_listar')

    info_acad_form = DirigenteFormacionAcademicaForm()

    if request.method == 'POST':
        info_acad_form = DirigenteFormacionAcademicaForm(request.POST)

        if info_acad_form.is_valid():
            inf_academ_nuevo = info_acad_form.save(commit=False)
            inf_academ_nuevo.dirigente = dirigente
            inf_academ_nuevo.save()
            info_acad_form.save()
            return redirect('dirigentes_formacion_academica', dirigente_id=dirigente_id, edicion=edicion)

    return render(request, 'dirigentes/wizard/wizard_formacion_academica.html', {
        'titulo': 'Formación académica',
        'wizard_stage': 4,
        'form': info_acad_form,
        'historicos': info_acad,
        'dirigente_id': dirigente_id,
        'edicion':edicion
    })

@login_required
@all_permission_required('snd.add_dirigente')
def eliminar_formacion_academica(request):
    pass

@login_required
def listar(request):
    """
    Junio 14 / 2015
    Autor: Cristian Leonardo Ríos López
    
    listar los dirigentes de la respectiva entidad

    Se obtienen los dirigentes que ha registrado la entidad que realiza la petición

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    return render(request, 'dirigentes/dirigentes_lista.html', {
        'tipo_tenant':request.tenant.tipo
    })

@login_required
@all_permission_required('snd.add_dirigente')
def finalizar(request, opcion, edicion):
    """
    Junio 14 / 2015
    Autor: Cristian Leonardo Ríos López
    
    enviar mensaje de finalizada la creación del dirigente


    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param opcion: indica si se quiere ir a listar o a registrar un dirigente nueno
    :type opcion: String
    :param edicion: indica si se está editando un dirigente existente o si se está registrando un dirigente nuevo
    :type edicion: Integer
    """

    if int(edicion):
        messages.success(request, "Dirigente editado correctamente.")
    else:
        messages.success(request, "Dirigente registrado correctamente.")

    try:
        del request.session['datos']
    except:
        pass

    if opcion == "nuevo":
        return redirect('dirigentes_nuevo')
    elif opcion == "listar":
        return redirect('dirigentes_listar')

@login_required
@all_permission_required('snd.add_dirigente')
def activar_desactivar(request, dirigente_id):
    """
    Junio 14 / 2015
    Autor: Cristian Leonardo Ríos López
    
    activar/desactivar dirigente

    Se obtienen el estado actual del dirigente y se invierte.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param dirigente_id:   Identificador del dirigente
    :type dirigente_id:    String
    """

    dirigente = Dirigente.objects.get(id=dirigente_id)
    estado_actual = dirigente.estado
    dirigente.estado = int(not(estado_actual))
    dirigente.save()
    if(estado_actual):
        message = "Dirigente activado correctamente."
    else:
        message = "Dirigente desactivado correctamente."
    messages.success(request, message)
    return redirect('dirigentes_listar')

@login_required
def ver(request, dirigente_id,id_entidad):
    """
    Junio 21 / 2015
    Autor: Cristian Leonardo Ríos López
    
    ver dirigente

    Se obtienen toda la información registrada del dirigente dado y se muestra.

    Edición: Septiembre 1 /2015
    NOTA: Para esta funcionalidad se empezó a pedir la entidad para conectarse y obtener la información de un objeto
    desde la entidad correcta, esto para efectos de consulta desde una liga o una federación.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param dirigente_id:   Identificador del dirigente
    :type dirigente_id:    String
    :param id_entidad: Llave primaria de la entidad a la que pertenece el personal de apoyo
    :type id_entidad: String
    """
    tenant = Entidad.objects.get(id=id_entidad).obtenerTenant()
    connection.set_tenant(tenant)
    ContentType.objects.clear_cache()
    try:
        dirigente = Dirigente.objects.get(id=dirigente_id)
    except Dirigente.DoesNotExist:
        messages.error(request, 'El dirigente que desea ver no existe')
        return redirect('dirigentes_listar')

    cargos = DirigenteCargo.objects.filter(dirigente=dirigente)
    for cargo in cargos:
        cargo.funciones = DirigenteFuncion.objects.filter(dirigente=dirigente, cargo=cargo.id)

    return render(request, 'dirigentes/dirigentes_ver.html', {
        'dirigente': dirigente,
        'cargos': cargos
    })


@login_required
@all_permission_required('snd.add_dirigente')
def verificar(request):
    """
    Julio 28 /2015
    Autor: Milton Lenis

    Verificación de la existencia de un dirigente
    Se verifica si existe el dirigente en la entidad actual o si no existe.
    Dependiendo del caso se muestra una respuesta diferente al usuario

    :param request: Petición Realizada
    :type request: WSGIRequest
    """
    if request.method=='POST':
        form = DirigenteVerificarExistenciaForm(request.POST)

        if form.is_valid():
            datos = {
                'identificacion': form.cleaned_data['identificacion'],
                'tipo_identificacion': form.cleaned_data['tipo_identificacion']
            }

            #Verificación de existencia dentro del tenant actual
            try:
                dirigente = Dirigente.objects.get(identificacion=datos['identificacion'],tipo_identificacion=datos['tipo_identificacion'])
            except Exception:
                dirigente = None

            if dirigente:
                #Si se encuentra el dirigente se carga el template con la existe=True para desplegar el aviso al usuario
                return render(request,'dirigentes/dirigentes_verificar.html',{'existe':True,
                                                                             'dirigente':dirigente})

            else:
                #Si no se encuentra el dirigente entonces se redirecciona a registro de dirigente con los datos iniciales en una sesión
                request.session['datos'] = datos
                #print(request.session)
                return redirect('dirigentes_nuevo')

    else:
        form = DirigenteVerificarExistenciaForm()
    return render(request,'dirigentes/dirigentes_verificar.html',{'form':form,
                                                                 'existe':False})
