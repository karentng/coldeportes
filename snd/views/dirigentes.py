from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from formtools.wizard.views import *
from snd.formularios.dirigentes  import *
from django.core.files.storage import FileSystemStorage
from django.conf import settings

@login_required
def wizard_identificacion_nuevo(request):
    """
    Junio 14 / 2015
    Autor: Cristian Leonardo Ríos López
    
    Crear un Dirigente

    Se obtienen los formularios de información del dirigente con los datos diligenciados y se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """

    identificacion_form = DirigenteForm( )

    if request.method == 'POST':

        identificacion_form = DirigenteForm(request.POST, request.FILES)

        if identificacion_form.is_valid():
            dirigente = identificacion_form.save(commit=False)
            dirigente.entidad =  request.tenant
            dirigente.save()
            identificacion_form.save()
            return redirect('dirigentes_wizard_funciones', dirigente.id)


    return render(request, 'dirigentes/wizard/wizard_identificacion.html', {
        'wizard_stage': 1,
        'form': identificacion_form,
    })

@login_required
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
    except Exception:
        dirigente = None

    identificacion_form = DirigenteForm(instance=dirigente)

    if request.method == 'POST':

        identificacion_form = DirigenteForm(request.POST, request.FILES, instance=dirigente)

        if identificacion_form.is_valid():
            identificacion_form.save()
            return redirect('dirigentes_wizard_funciones', dirigente_id)


    return render(request, 'dirigentes/wizard/wizard_identificacion.html', {
        'wizard_stage': 1,
        'form': identificacion_form,
    })

@login_required
def wizard_funciones(request, dirigente_id):
    """
    Junio 14 / 2015
    Autor: Cristian Leonardo Ríos López
    
    Funciones del cargo de un dirigente

    Se obtienen el formulario de las funciones del cargo y se muestran las funciones actualmente añadidas al dirigente
    y si hay modificaciones se guardan.
    Si el dirigente es nuevo se inicializa en nulo.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param dirigente_id:   Identificador del dirigente
    :type dirigente_id:    String
    """

    try:
        funciones = Funcion.objects.filter(dirigente=dirigente_id)
    except Exception:
        funciones = None

    funciones_form = DirigenteFuncionesForm()

    if request.method == 'POST':
        funciones_form = DirigenteFuncionesForm(request.POST)

        if funciones_form.is_valid():
            funcion_nueva = funciones_form.save(commit=False)
            funcion_nueva.dirigente = Dirigente.objects.get(id=dirigente_id)
            funcion_nueva.save()
            #funciones_form.save()#<PENDIENTE> por qué se guarda el form
            return redirect('dirigentes_wizard_funciones', dirigente_id)

    return render(request, 'dirigentes/wizard/wizard_funciones.html', {
        'wizard_stage': 2,
        'form': funciones_form,
        'funciones': funciones,
        'dirigente_id': dirigente_id
    })

@login_required
def eliminar_funcion(request, dirigente_id, funcion_id):
    """
    Junio 14 / 2015
    Autor: Cristian Leonardo Ríos López
    
    Eliminar función

    Se obtienen la función de la base de datos y se elimina

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param dirigente_id:   Identificador del dirigente
    :type escenario_id:    String
    :param funcion_id   Identificador de la función
    :type funcion_id    String
    """

    try:
        funcion = Funcion.objects.get(id=funcion_id, dirigente=dirigente_id)
        funcion.delete()
        return redirect('dirigentes_wizard_funciones', dirigente_id)

    except Exception:
        return redirect('dirigentes_wizard_funciones', dirigente_id)

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
    dirigentes = Dirigente.objects.all()
    return render(request, 'dirigentes/dirigentes_lista.html', {
        'dirigentes': dirigentes,
    })

@login_required
def finalizar(request, opcion):
    """
    Junio 14 / 2015
    Autor: Cristian Leonardo Ríos López
    
    enviar mensaje de finalizada la creación del dirigente


    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    messages.success(request, "Dirigente registrado correctamente.")
    
    if opcion == "nuevo":
        return redirect('dirigentes_wizard_identificacion_nuevo')
    elif opcion == "listar":
        return redirect('dirigentes_listar')

@login_required
def activar_desactivar(request, dirigente_id):
    """
    Junio 14 / 2015
    Autor: Cristian Leonardo Ríos López
    
    activar/desactivar dirigente

    Se obtienen el estado actual del escenario y se invierte.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param dirigente_id:   Identificador del dirigente
    :type dirigente_id:    String
    """
    dirigente = Dirigente.objects.get(id=dirigente_id)
    estado_actual = dirigente.activo
    dirigente.activo = not(estado_actual)
    dirigente.save()
    if(estado_actual):
        message = "Dirigente desactivado correctamente."
    else:
        message = "Dirigente activado correctamente."
    messages.warning(request, message)
    return redirect('dirigentes_listar')

@login_required
def ver(request, dirigente_id):
    """
    Junio 21 / 2015
    Autor: Cristian Leonardo Ríos López
    
    ver dirigente

    Se obtienen toda la información registrada del dirigente dado y se muestra.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param dirigente_id:   Identificador del dirigente
    :type dirigente_id:    String
    """

    dirigente = Dirigente.objects.get(id=dirigente_id)
    funciones = Funcion.objects.filter(dirigente=dirigente)

    return render(request, 'dirigentes/dirigentes_ver.html', {
        'dirigente': dirigente,
        'funciones': funciones
    })