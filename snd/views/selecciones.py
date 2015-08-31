from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from snd.formularios.selecciones import *
from django.contrib import messages
from snd.models import *
from entidades.models import *
from django.http import JsonResponse

@login_required
def registrar_base(request):
    """
    Agosto 29 / 2015
    Autor: Daniel Correa

    Permite guardar la primera seccion de la seleccion dando paso a la seleccion de deportistas y personal de apoyo

    :param request: Petición Realizada
    :type request: WSGIRequest
    """

    form = SeleccionForm(initial={'tipo':request.tenant.tipo})

    if request.method == 'POST':
        form = SeleccionForm(request.tenant.tipo,request.POST)
        if form.is_valid():
            sele = form.save()
            return redirect('registrar_deportistas',sele.id)

    return render(request,'selecciones/wizard/wizard_seleccion.html',{
        'titulo': 'Selección',
        'form': form,
        'wizard_stage': 1
    })

@login_required
def registrar_deportistas(request,id_s):
    """
    Agosto 31 / 2015
    Autor: Daniel Correa

    Permite registrar los deportistas de una seleccion

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_s: id de la seleccion a la cual asignar deportistas
    :type id_s: string
    """

    try:
        sele = Seleccion.objects.get(id=id_s)
    except:
        messages.error(request,'No existe la selección solicitada')
        return redirect('listar_seleccion')

    deportistas = []
    if request.tenant.tipo == 1:
        #Liga
        clubes = Club.objects.filter(liga=request.tenant.id)
        for c in clubes:
            connection.set_tenant(c)
            ContentType.objects.clear_cache()
            deportistas += Deportista.objects.filter(estado=0)
        connection.set_tenant(request.tenant)
    elif request.tenant.tipo == 2:
        #Fede
        pass
    else:
        messages.error(request,'Usted esta en una sección que no le corresponde')
        return redirect('inicio_tenant')

    #depor_seleccionados = DeportistasSeleccion.objects.filter(seleccion=sele)
    depor_registrados = []
    #depor_registrados = [Deportista.objects.get(id=x.deportista) for x in depor_seleccionados]

    return render(request,'selecciones/wizard/wizard_seleccion_deportistas.html',{
        'titulo': 'Selección de Deportistas',
        'wizard_stage': 2,
        'deportistas': deportistas,
        'sele_id': sele.id,
        'depor_registrados': depor_registrados
    })

@login_required
def registrar_personal(request,id_s):
    return redirect('inicio_tenant')

@login_required
def listar_seleccion(request):
    """
    Agosto 30 / 2015
    Autor: Daniel Correa

    Permite listar todas las selecciones con la estrategia de cargue masivo

    :param request: Petición Realizada
    :type request: WSGIRequest
    """

    selecciones = Seleccion.objects.all()

    return render(request,'selecciones/listar_selecciones.html',{
        'selecciones': selecciones
    })

#AJAX SELECCIONES

#AJAX SELECCION DE DEPORTISTAS
@login_required
def vista_previa_deportista(request,id_entidad,id_depor):
    """
    Agosto 31 / 2015
    Autor: Daniel Correa

    Permite obtener la vista previa del deportista a seleccionar

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_entidad: id entidad a traer deportista
    :param id_depor: id deportistas a mostrar
    """
    try:
        ent = Entidad.objects.get(id=id_entidad)
    except:
        messages.error(request,'Entidad no encontrada')
        return redirect('listar_seleccion')

    connection.set_tenant(ent)
    ContentType.objects.clear_cache()

    try:
        depor = Deportista.objects.get(id=id_depor)
    except:
        messages.error(request,'Deportista no existe')
        return redirect('listar_seleccion')

    return render(request,'selecciones/wizard/ajax_seleccion_deportistas/vista_previa.html',{
        'deportista': depor
    })

@login_required
def seleccionar_deportista(request,id_s,id_entidad,id_depor):
    """
    Agosto 31 / 2015
    Autor: Daniel Correa

    Permite guardar los deportistas seleccionados de la seleccion id_s

    :param request:
    :param id_s:
    :param id_entidad:
    :param id_depor:
    :return:
    """
    try:
        ent = Entidad.objects.get(id=id_entidad)
    except:
        messages.error(request,'Entidad no encontrada')
        return redirect('listar_seleccion')

    connection.set_tenant(ent)
    ContentType.objects.clear_cache()

    try:
        depor = Deportista.objects.get(id=id_depor)
    except:
        messages.error(request,'Deportista no existe')
        return redirect('listar_seleccion')

    connection.set_tenant(request.tenant)

    try:
        sele = Seleccion.objects.get(id=id_s)
    except:
        messages.error(request,'No existe la seleccion solicitada')
        return redirect('listar_seleccion')

    depor_sele = DeportistasSeleccion(deportista=depor.id,entidad=ent,seleccion=sele)
    depor_sele.save()

    return JsonResponse({
        'respuesta': [depor.nombres + ' ' +depor.apellidos,depor.tipo_id,depor.identificacion,depor.edad(),depor.ciudad_residencia.__str__(),depor.entidad.nombre,]
    })
