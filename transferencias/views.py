from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from entidades.models import Entidad
from snd.models import InformacionAdicional,HistorialLesiones,HistorialDoping,Deportista,Escenario,PersonalApoyo,Foto,CaracterizacionEscenario,ComposicionCorporal,HistorialDeportivo,InformacionAcademica,FormacionDeportiva,ExperienciaLaboral,HorarioDisponibilidad,Video,DatoHistorico,Contacto,CambioDocumentoDeportista
from snd.formularios.deportistas import  DeportistaForm
from .models import Transferencia
import datetime
from coldeportes.utilities import calculate_age,not_transferido_required
# Create your views here.
@login_required
def generar_transferencia(request,id):
    """
    Julio 15, 2015
    Autor: Daniel Correa

    Transferencia de objetos entre entidades, esta definida la transferencia de personas (Deportistas, Personal de apoyo) y Escenarios
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

    if entidad_solicitante.tipo == 3:
        entidades = Entidad.objects.filter(tipo=3).exclude(nombre=entidad_solicitante.nombre).exclude(schema_name='public')
    elif entidad_solicitante.tipo == 9:
        entidades = Entidad.objects.filter(tipo=9).exclude(nombre=entidad_solicitante.nombre).exclude(schema_name='public')
    else:
        messages.error(request,'Usted se encuentra en una seccion que no le corresponde')
        return redirect('inicio_tenant')

    try:
        objeto = Deportista.objects.get(id=id)
    except:
        messages.error(request,'Error, no existe objeto transferible')

    non_permission = not_transferido_required(request,objeto)
    if non_permission:
        return non_permission

    objeto.fecha = datetime.date.today()
    objeto.tipo_objeto = objeto.__class__.__name__

    if request.method == 'POST':
        id_entidad_cambio = request.POST['entidad']
        entidad_cambio = Entidad.objects.get(id=id_entidad_cambio)
        connection.set_tenant(entidad_cambio)
        ContentType.objects.clear_cache()
        transferencia = Transferencia(
            entidad=entidad_solicitante,
            fecha_solicitud = objeto.fecha,
            id_objeto = objeto.id,
            tipo_objeto = objeto.tipo_objeto
        )
        transferencia.save()
        #Cambiar estado de objeto a "En Transferencia"
        connection.set_tenant(request.tenant)
        ContentType.objects.clear_cache()
        objeto.estado = 2
        objeto.save()
        #
        messages.success(request,'Transferencia generada exitosamente, se le informara cuando la entidad acepte su solicitud')
        return redirect('deportista_listar')

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
    id_obj = transferencia.id_objeto
    objeto,adicionales = obtener_objeto(id_obj,tipo_objeto)

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
        return redirect('inicio_tenant')
    else:
        #Acepto transferencia

        connection.set_tenant(request.tenant)
        ContentType.objects.clear_cache()

        #Posibilidad de cambio de documento de deportista
        existe,match = existencia_caso_cambio_tipo_id(request,objeto,tipo_objeto,entidad_cambio)

        if existe:
            id_old = match.identificacion
            match.identificacion = objeto.identificacion
            match.tipo_id = objeto.tipo_id
            match.entidad = request.tenant
            match.estado = 0

            obj_dict = match.__dict__
            del obj_dict['id']
            del obj_dict['_entidad_cache']
            del obj_dict['_state']

            deportista, created = Deportista.objects.update_or_create(
                identificacion=id_old,
                defaults= obj_dict,
            )
            deportista.nacionalidades_obj = objeto.nacionalidades_obj
            deportista.disciplinas_obj = objeto.disciplinas_obj
            deportista.entidad = request.tenant
            transferido = guardar_objeto(deportista,adicionales,tipo_objeto)
            messages.success(request,'Transferencia recibida exitosamente')

        else:
            objeto.entidad = request.tenant
            objeto.estado = 0
            transferido = guardar_objeto(objeto,adicionales,tipo_objeto)
            messages.success(request,'Transferencia recibida exitosamente')

    return finalizar_transferencia(request,entidad_cambio,transferido,transferencia)

def existencia_caso_cambio_tipo_id(request,objeto,tipo_objeto,entidad_saliente):
    """
    Agosto 13, 2015
    Autor: Daniel Correa

    Permite conocer si este caso de transferencia es un caso de cambio de documento por parte del deportista, es decir , el caso especial en transferencias:
    Un deportista es transferido de la entidad Y a la entidad X , en dicha entidad cambia de tipo de documento , vuelve a la entidad Y, se debe verificar su existencia como transferido
    para evitar registros duplicados

    :param objeto: objeto transferible
    :type id: string
    :param tipo_objeto: tipo del objeto transferible
    :type tipo_objeto: string
    :return:
    """
    if tipo_objeto == 'Deportista':
        try:
           Deportista.objects.get(identificacion=objeto.identificacion)
        except:
            posibilidades = list(Deportista.objects.filter(nombres=objeto.nombres, apellidos=objeto.apellidos).exclude(tipo_id=objeto.tipo_id))
            if len(posibilidades) == 0:
                return False,None
            else:
                connection.set_tenant(entidad_saliente)
                ContentType.objects.clear_cache()
                for p in posibilidades:
                    id_old = p.identificacion
                    tipo_old = p.tipo_id
                    try:
                        CambioDocumentoDeportista.objects.get(deportista=objeto,tipo_documento_anterior=tipo_old,identificacion_anterior=id_old)
                        connection.set_tenant(request.tenant)
                        ContentType.objects.clear_cache()
                        return True,p
                    except:
                        pass
                connection.set_tenant(request.tenant)
                ContentType.objects.clear_cache()

    return False,None

def finalizar_transferencia(request,entidad_saliente,objeto,transferencia):
    """
    Agosto 12, 2015
    Autor: Daniel Correa

    Función que permite finalizar la transferencia una vez es aceptada

    :param request: request
    :param entidad_saliente: entidad de donde vino el objeto transferible
    :param objeto: objeto transferible
    :param tipo_objeto: tipo del objeto transferible
    :param transferencia: objeto transferencia
    :return: render con la pagina de aprobación
    """
    transferencia.estado = 'Aprobada'
    transferencia.save()

    connection.set_tenant(entidad_saliente)
    ContentType.objects.clear_cache()

    depor = Deportista.objects.get(identificacion=objeto.identificacion,tipo_id = objeto.tipo_id)
    depor.estado = 3
    depor.entidad = request.tenant
    depor.save()
    depor.tipo_objeto = "Deportista"
    depor.fecha = datetime.date.today()

    return render(request,'transferencia_exitosa.html',{
        'objeto': objeto
    })

def guardar_objeto(objeto,adicionales,tipo):
    """
    Agosto 8, 2015
    Autor: Daniel Correa

    Permite guardar el objeto transferido dependiendo del tipo y sus propiedades

    :param objeto: objeto a guardar
    :param adicionales: informacion adicional al objeto
    :param tipo: tipo de objeto
    """

    if tipo == 'Deportista':

        nacionalidades_obj = objeto.nacionalidades_obj
        disciplinas_obj = objeto.disciplinas_obj
        #Diccionario para defaults
        obj_dict = objeto.__dict__
        del obj_dict['id']
        del obj_dict['_entidad_cache']
        del obj_dict['disciplinas_obj']
        del obj_dict['nacionalidades_obj']
        del obj_dict['_state']
        #Fin diccionario
        deportista, created = Deportista.objects.update_or_create(
            identificacion=objeto.identificacion,
            defaults= obj_dict,
        )

        for na in nacionalidades_obj:
            deportista.nacionalidad.add(na)

        for di in disciplinas_obj:
            deportista.disciplinas.add(di)

        for ad in adicionales:
            diccionario = ad.__dict__
            del diccionario['id']
            del diccionario['_state']
            del diccionario['deportista_id']
            if type(ad) is HistorialDeportivo:
                HistorialDeportivo.objects.update_or_create(
                    deportista=deportista,
                    nombre=ad.nombre,
                    modalidad=ad.modalidad,
                    division=ad.division,
                    prueba=ad.prueba,
                    categoria=ad.categoria,
                    defaults=diccionario
                )
            elif type(ad) is InformacionAdicional:
                InformacionAdicional.objects.update_or_create(
                    deportista=deportista,
                    defaults=diccionario
                )
            elif type(ad) is HistorialLesiones:
                HistorialLesiones.objects.update_or_create(
                    deportista=deportista,
                    defaults=diccionario
                )
            elif type(ad) is HistorialDoping:
                HistorialDoping.objects.update_or_create(
                    deportista=deportista,
                    defaults=diccionario
                )
            elif type(ad) is InformacionAcademica:
                InformacionAcademica.objects.update_or_create(
                    deportista=deportista,
                    institucion=ad.institucion,
                    nivel=ad.nivel,
                    profesion=ad.profesion,
                    defaults=diccionario
                )
            else:
                ComposicionCorporal.objects.update_or_create(
                    deportista=deportista,
                    defaults=diccionario
                )
        return deportista

def obtener_objeto(id_obj,tipo_objeto):
    """
    Agosto 6, 2015
    Autor: Daniel Correa

    Permite obtener los datos de un objeto para su procesamiento de transferencia

    :param id: id del objeto transferible
    :type id: string
    :param tipo_objeto: tipo del objeto transferible
    :type tipo_objeto: string
    :return:
    """

    objeto = None
    adicionales = []
    #Seleccion del objeto
    if tipo_objeto =='Deportista':

        objeto = Deportista.objects.get(id=id_obj)

        #Obtener muchos a muchos y guardarlos como attr apartes
        objeto.nacionalidades_obj = [a for a in objeto.nacionalidad.all()]
        objeto.disciplinas_obj = [b for b in objeto.disciplinas.all()]
        #Fin obtener muchos a muchos y guardarlos como attr apartes

        adicionales += ComposicionCorporal.objects.filter(deportista=objeto)
        adicionales += HistorialDeportivo.objects.filter(deportista=objeto)
        adicionales += InformacionAcademica.objects.filter(deportista=objeto)
        adicionales += InformacionAdicional.objects.filter(deportista=objeto)
        adicionales += HistorialLesiones.objects.filter(deportista=objeto)
        adicionales += HistorialDoping.objects.filter(deportista=objeto)

    return objeto,adicionales

@login_required
def cancelar_transferencia(request,id_objeto):
    """
    Julio 21, 2015
    Autor: Daniel Correa

    Funcion para calcelacion de transferencia por parte del solicitante, el protocolo para conocer que clase de objeto es el que se solicita su cancelacion es:
    1 para Deportista, 2 para PersonalApoyo, 3 para Escenario

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_objeto: Id del objeto a cancelar la transferencia
    :type id_objeto: stirng
    :param tipo_objeto: Tipo del objeto de acuerdo al protocolo
    :type tipo_objeto: string
    """

    try:
        obj_trans = Deportista.objects.get(id=id_objeto)
    except:
        messages.error(request,'Error: No se puede procesar la solicitud, Deportista no existe')
        return redirect('deportista_listar')

    entidad_solicitante = request.tenant
    entidades = Entidad.objects.exclude(schema_name__in=['public',entidad_solicitante.schema_name])

    string = ""
    from django.http import HttpResponse
    for ent in entidades:
        try:
            string += ent.schema_name +" "+ent.nombre+" || "
            connection.set_tenant(ent)
            ContentType.objects.clear_cache()
            trans = Transferencia.objects.filter(id_objeto=id_objeto,estado='Pendiente',entidad=entidad_solicitante,tipo_objeto='Deportista')

            if len(trans) != 0:
                trans.delete()
                connection.set_tenant(entidad_solicitante)
                obj_trans.estado = 0
                obj_trans.save()
                messages.success(request,'Tranferencia cancelada exitosamente')
                return redirect('deportista_listar')
        except Exception as e:
            string += str(e)
            return HttpResponse(string)

    messages.error(request,'Error: No existe la transferencia solicitada, La entidad a la cual se envío el deportista ya proceso la transferencia pendiente')
    return redirect('deportista_listar')