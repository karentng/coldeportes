from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from entidades.models import Entidad
from snd.models import Deportista,Escenario,Entrenador,Foto,CaracterizacionEscenario
from .models import Transferencia
import datetime
from coldeportes.utilities import calculate_age
# Create your views here.
@login_required
def generar_transferencia(request,tipo_transfer,tipo_persona,id):
    """
    Julio 15, 2015
    Autor: Daniel Correa

    Transferencia de objetos entre entidades, esta definida la transferencia de personas (Deportistas, Entrenadores) y Escenarios
    Dentro de personas el protocolo es , 1 para Deportistas y 2 para Enetrenadores

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param tipo_transfer: Tipo de transferencia, el protocolo define 1 para personas y 2 para escenarios
    :type tipo_transfer: int
    :param tipo_persona: Tipo de persona, el protocolo define 1 para Deportistas y 2 para Enetrenadores
    :type tipo_persona: int
    :param id: Identificacion de objeto a tranferir
    :type id: String
    """
    objeto = None
    entidad_solicitante = request.tenant
    entidades = Entidad.objects.exclude(nombre__in=['publico',entidad_solicitante.nombre])
    redir = ''
    if tipo_transfer=='1': #Transferencia de personas
        if tipo_persona=='1': #Transferencia de deportistas
            objeto = Deportista.objects.get(id=id)
            objeto.tipo_objeto='Deportista'
            redir='deportista_listar'
        elif tipo_persona=='2': #Transferencia de entrenadores
            objeto = Entrenador.objects.get(id=id)
            objeto.tipo_objeto='Entrenador'
            redir='entrenador_listar'
        objeto.edad = calculate_age(objeto.fecha_nacimiento)
        objeto.nacionalidad_str = ",".join(str(x) for x in objeto.nacionalidad.all())
        objeto.fotos = [objeto.foto]
    elif tipo_transfer=='2': #Transferencia de escenarios
        objeto = Escenario.objects.get(id=id)
        fotos = [x.foto for x in Foto.objects.filter(escenario=objeto)]
        caracteristicas = CaracterizacionEscenario.objects.get(escenario=objeto)
        objeto.capacidad = caracteristicas.capacidad_espectadores
        objeto.tipo_escenario = caracteristicas.tipo_escenario
        objeto.fotos=fotos
        objeto.tipo_objeto='Escenario'
        redir='listar_escenarios'

    objeto.fecha = datetime.date.today()
    objeto.entidad = entidad_solicitante
    if request.method == 'POST':
        id_entidad_cambio = request.POST['entidad']
        entidad_cambio = Entidad.objects.get(id=id_entidad_cambio)
        connection.set_tenant(entidad_cambio)
        ContentType.objects.clear_cache()
        transferencia = Transferencia()
        transferencia.entidad = entidad_solicitante
        transferencia.fecha_solicitud = objeto.fecha
        transferencia.id_objeto = objeto.id
        transferencia.tipo_objeto = objeto.tipo_objeto
        transferencia.save()
        #
        #Cambiar estado de objeto a "En Transferencia"
        connection.set_tenant(request.tenant)
        ContentType.objects.clear_cache()
        objeto.estado = 2
        objeto.save()
        #
        messages.success(request,'Transferencia generada exitosamente, se le informara cuando la entidad acepte su solicitud')
        return redirect(redir)

    return render(request,'generar_transferencia.html',{
        'entidades' : entidades,
        'objeto' : objeto
    })

@login_required
def procesar_transferencia(request,id_transfer,opcion):
    """
    Julio 31, 2015
    Autor: Daniel Correa

    Función para procesar una transferencia , ya sea rechazarla o aceptarla. El protocolo dice 0 para rechazar 1 para aceptar

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_transfer: Identificacion del objeto transferencia
    :type id_transfer: int
    :param opcion: Opcion elegida, 0 rechazo, 1 acepto
    :type opcion: string
    """
    try:
        transferencia = Transferencia.objects.get(id=id_transfer)
    except:
        messages.error(request,'Transferencia no encontrada')
        return redirect('inicio_tenant')

    entidad_cambio = transferencia.entidad
    connection.set_tenant(entidad_cambio)
    ContentType.objects.clear_cache()

    tipo_objeto = transferencia.tipo_objeto
    objeto = None
    #Seleccion del objeto
    if tipo_objeto=='Deportista':
        objeto =  Deportista.objects.get(id=transferencia.id_objeto)
    elif tipo_objeto == 'Entrenador':
        objeto = Entrenador.objects.get(id=transferencia.id_objeto)
    elif tipo_objeto== 'Escenario':
        objeto = Escenario.objects.get(id=transferencia.id_objeto)

    #Procesamiento del objeto
    if opcion == '0':
        #Rechazo de transferencia
        objeto.estado = 0
        objeto.save()

        connection.set_tenant(request.tenant)
        ContentType.objects.clear_cache()

        transferencia.estado = 'Rechazada'
        transferencia.save()

        messages.warning(request,'Transferencia rechazada exitosamente')
    else:
        #Aceptacion de transferencia
        pass
        messages.success(request,'Transferencia procesada exitosamente')

    return redirect('inicio_tenant')

@login_required
def cancelar_transferencia(request,id_objeto,tipo_objeto):
    """
    Julio 21, 2015
    Autor: Daniel Correa

    Funcion para calcelacion de transferencia por parte del solicitante, el protocolo para conocer que clase de objeto es el que se solicita su cancelacion es:
    1 para Deportista, 2 para Entrenador, 3 para Escenario

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_objeto: Id del objeto a cancelar la transferencia
    :type id_objeto: stirng
    :param tipo_objeto: Tipo del objeto de acuerdo al protocolo
    :type tipo_objeto: string
    """

    objeto = ''
    if tipo_objeto=='1':
        objeto = 'Deportista'
        redir = 'deportista_listar'
        try:
            depor = Deportista.objects.get(id=id_objeto)
            depor.estado = 0
            depor.save()
        except:
            messages.error(request,'Error: No se puede procesar la solicitud, Deportista no existe')
            return redirect(redir)
    elif tipo_objeto=='2':
        objeto='Entrenador'
        redir='entrenador_listar'
        try:
            entre = Entrenador.objects.get(id=id_objeto)
            entre.estado = 0
            entre.save()
        except:
            messages.error(request,'Error: No se puede procesar la solicitud, Entrenador no existe')
            return redirect(redir)
    elif tipo_objeto=='3':
        objeto='Escenario'
        redir='listar_escenarios'
        try:
            esce = Escenario.objects.get(id=id_objeto)
            esce.estado = 0
            esce.save()
        except:
            messages.error(request,'Error: No se puede procesar la solicitud, Escenario no existe')
            return redirect(redir)

    entidad_solicitante = request.tenant
    entidades = Entidad.objects.exclude(nombre__in=['publico',entidad_solicitante.nombre])

    for ent in entidades:
        connection.set_tenant(ent)
        ContentType.objects.clear_cache()
        trans = Transferencia.objects.filter(id_objeto=id_objeto,estado='Pendiente',entidad=entidad_solicitante,tipo_objeto=objeto)
        if len(trans) != 0:
            trans.delete()
            messages.success(request,'Tranferencia cancelada exitosamente')
            return redirect(redir)

    messages.error(request,'Error: No existe la transferencia solicitada')
    return redirect(redir)