from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from entidades.models import Entidad
from snd.models import Deportista,Escenario,PersonalApoyo,Foto,CaracterizacionEscenario,ComposicionCorporal,HistorialDeportivo,InformacionAcademica,FormacionDeportiva,ExperienciaLaboral,HorarioDisponibilidad,Video,DatoHistorico,Contacto
from snd.formularios.deportistas import DeportistaForm,ComposicionCorporalForm,HistorialDeportivoForm,InformacionAcademicaForm
from .models import Transferencia
import datetime
from coldeportes.utilities import calculate_age
# Create your views here.
@login_required
def generar_transferencia(request,tipo_transfer,tipo_persona,id):
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
    entidades = Entidad.objects.exclude(nombre__in=['publico',entidad_solicitante.nombre])
    redir = ''
    if tipo_transfer=='1': #Transferencia de personas
        if tipo_persona=='1': #Transferencia de deportistas
            objeto = Deportista.objects.get(id=id)
            objeto.tipo_objeto='Deportista'
            redir='deportista_listar'
        elif tipo_persona=='2': #Transferencia de personal_apoyo
            objeto = PersonalApoyo.objects.get(id=id)
            objeto.tipo_objeto='PersonalApoyo'
            redir='personal_apoyo_listar'
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
    else:
        #Acepto transferencia

        connection.set_tenant(request.tenant)
        ContentType.objects.clear_cache()

        existe,posibilidades = existencia_objeto(objeto,tipo_objeto)

        if existe:
            pass

        else:
            objeto.entidad = request.tenant
            objeto.entidad_vinculacion = request.tenant #quitar luego de cambio
            objeto.estado = 0
            guardar_objeto(objeto,adicionales,tipo_objeto)

    return finalizar_transferencia(request,entidad_cambio,objeto,tipo_objeto,transferencia)

def finalizar_transferencia(request,entidad_saliente,objeto,tipo_objeto,transferencia):

    transferencia.estado = 'Aprobada'
    transferencia.save()

    connection.set_tenant(entidad_saliente)
    ContentType.objects.clear_cache()

    objeto.estado = 3
    if tipo_objeto=='Deportista' or tipo_objeto=='PersonalApoyo':
        new_obj, created = objeto.__class__.objects.update_or_create(
            identificacion = objeto.identificacion,
            defaults=objeto.__dict__
        )
        new_obj.edad = calculate_age(new_obj.fecha_nacimiento)
        new_obj.nacionalidad_str = ",".join(str(x) for x in new_obj.nacionalidad.all())
        new_obj.fotos = [new_obj.foto]
    else:
        new_obj, created =  objeto.__class__.objects.update_or_create(
            nombre=objeto.nombre,
            defaults=objeto.__dict__
        )
        fotos = [x.foto for x in Foto.objects.filter(escenario=new_obj)]
        caracteristicas = CaracterizacionEscenario.objects.get(escenario=new_obj)
        new_obj.capacidad = caracteristicas.capacidad_espectadores
        new_obj.tipo_escenario = caracteristicas.tipo_escenario
        new_obj.fotos=fotos

    new_obj.tipo_objeto = new_obj.__class__.__name__
    new_obj.fecha = datetime.date.today()
    new_obj.entidad_sol = entidad_saliente

    return render(request,'transferencia_exitosa.html',{
        'objeto': new_obj
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
        del obj_dict['entidad_vinculacion'] #quitar luego de cambio
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
            elif type(ad) is InformacionAcademica:
                print()
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

    elif tipo == 'PersonalApoyo':

        nacionalidades_obj = objeto.nacionalidades_obj

        #Diccionario para defaults
        obj_dict = objeto.__dict__
        del obj_dict['id']
        del obj_dict['nacionalidades_obj']
        del obj_dict['_state']
        del obj_dict['entidad'] #quitar luego de cambio
        del obj_dict['_entidad_vinculacion_cache'] #quitar luego de cambio
        #Fin diccionario

        personal_apoyo, created = PersonalApoyo.objects.update_or_create(
            identificacion=objeto.identificacion,
            defaults= obj_dict,
        )

        for na in nacionalidades_obj:
            personal_apoyo.nacionalidad.add(na)

        for ad in adicionales:
            diccionario = ad.__dict__
            del diccionario['id']
            del diccionario['_state']
            del diccionario['personal_apoyo_id']
            if type(ad) is FormacionDeportiva: #cambiar luego del cambio de personal apoyo
                disciplinas_form = ad.disciplinas_form
                del diccionario['disciplinas_form']
                formacion, created = FormacionDeportiva.objects.update_or_create(
                    personal_apoyo=personal_apoyo,
                    denominacion_diploma=ad.denominacion_diploma,
                    defaults=diccionario
                )
                for disc in disciplinas_form:
                    formacion.disciplina_deportiva.add(disc)
            else:
                ExperienciaLaboral.objects.update_or_create(
                    personal_apoyo=personal_apoyo,
                    nombre_cargo=ad.nombre_cargo,
                    defaults=diccionario
                )

    elif tipo == 'Escenario':

        #Diccionario para defaults
        obj_dict = objeto.__dict__
        del obj_dict['id']
        del obj_dict['_entidad_cache']
        del obj_dict['_state']
        del obj_dict['entidad_vinculacion'] #quitar luego de cambio
        #Fin diccionario

        escenario, created = Escenario.objects.update_or_create(
            nombre=objeto.nombre,
            defaults= obj_dict,
        )
        for ad in adicionales:
            diccionario = ad.__dict__
            del diccionario['id']
            del diccionario['_state']
            del diccionario['escenario_id']
            if type(ad) is CaracterizacionEscenario:
                tipo_disciplinas_obj = ad.tipo_disciplinas_obj
                tipo_superficie_juego_obj= ad.tipo_superficie_juego_obj
                caracteristicas_obj=ad.caracteristicas_obj
                clase_uso_obj=ad.clase_uso_obj

                del diccionario['tipo_disciplinas_obj']
                del diccionario['tipo_superficie_juego_obj']
                del diccionario['caracteristicas_obj']
                del diccionario['clase_uso_obj']

                caracterizacion, created = CaracterizacionEscenario.objects.update_or_create(
                    escenario=escenario,
                    defaults=diccionario
                )
                for tipo_d in tipo_disciplinas_obj:
                    caracterizacion.tipo_disciplinas.add(tipo_d)
                for tipo_super in tipo_superficie_juego_obj:
                    caracterizacion.tipo_superficie_juego.add(tipo_super)
                for carac in caracteristicas_obj:
                    caracterizacion.caracteristicas.add(carac)
                for clase_uso in clase_uso_obj:
                    caracterizacion.clase_uso.add(clase_uso)

            elif type(ad) is HorarioDisponibilidad:
                dias_obj = ad.dias_obj

                del diccionario['dias_obj']

                horario, created = HorarioDisponibilidad.objects.update_or_create(
                    escenario=escenario,
                    descripcion=ad.descripcion,
                    defaults=diccionario
                )

                for di in dias_obj:
                    horario.dias.add(di)
            elif type(ad) is Foto:
                Foto.objects.update_or_create(
                    escenario=escenario,
                    foto=ad.foto,
                    defaults=diccionario
                )
            elif type(ad) is Video:
                Video.objects.update_or_create(
                    escenario=escenario,
                    url=ad.url,
                    defaults=diccionario
                )
            elif type(ad) is DatoHistorico:
                DatoHistorico.objects.update_or_create(
                    escenario=escenario,
                    descripcion=ad.descripcion,
                    defaults=diccionario
                )
            elif type(ad) is Contacto:
                Contacto.objects.update_or_create(
                    escenario=escenario,
                    nombre=ad.nombre,
                    defaults=diccionario
                )

def obtener_objeto(id_obj,tipo_objeto):
    """
    Agosto 6, 2015
    Autor: Daniel Correa

    Permite obtener los datos de un objeto para su procesamiento de transferencia

    :param id: id del objeto transferible
    :param tipo_objeto: tipo del objeto transferible
    :return:
    """

    objeto = None
    identificacion = ""
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

    elif tipo_objeto == 'PersonalApoyo':

        objeto = PersonalApoyo.objects.get(id=id_obj)

        #Obtener muchos a muchos y guardarlos como attr apartes
        objeto.nacionalidades_obj = [a for a in objeto.nacionalidad.all()]
        #Fin obtener muchos a muchos y guardarlos como attr apartes

        #Sacar y asignar muchos a muchos de formacion deportiva
        formaciones = FormacionDeportiva.objects.filter(personal_apoyo=objeto)
        for form in formaciones:
            form.disciplinas_form = [disc for disc in form.disciplina_deportiva.all()]
        #Fin sacar y asignar muchos a muchos de formacion deportiva

        adicionales += formaciones
        adicionales += ExperienciaLaboral.objects.filter(personal_apoyo=objeto)

    elif tipo_objeto == 'Escenario':

        objeto = Escenario.objects.get(id=id_obj)

        #Sacar y asignar muchos a muchos caracterizacion
        caracterizaciones = CaracterizacionEscenario.objects.filter(escenario=objeto)
        for car in caracterizaciones:
            car.tipo_disciplinas_obj = [x for x in car.tipo_disciplinas.all()]
            car.tipo_superficie_juego_obj = [x for x in car.tipo_superficie_juego.all()]
            car.caracteristicas_obj = [x for x in car.caracteristicas.all()]
            car.clase_uso_obj = [x for x in car.clase_uso.all()]
        #Fin sacar y asignar m2m caracteristicas

        adicionales += caracterizaciones

        #Sacar y asignar m2m a horarios
        horarios = HorarioDisponibilidad.objects.filter(escenario=objeto)
        for h in horarios:
            h.dias_obj = [x for x in h.dias.all()]
        #Fin sacar y asignar m2ma horarios

        adicionales += horarios
        adicionales += Foto.objects.filter(escenario=objeto)
        adicionales += Video.objects.filter(escenario=objeto)
        adicionales += DatoHistorico.objects.filter(escenario=objeto)
        adicionales += Contacto.objects.filter(escenario=objeto)

    return objeto,adicionales

def existencia_objeto(objeto,tipo_objeto):
    """
    Agosto 13, 2015
    Autor: Daniel Correa

    Permite conocer si este caso de transferencia es un caso de cambio de documento por parte del deportista, es decir , el caso especial en transferencias:
    Un deportista es transferido de la entidad Y a la entidad X , en dicha entidad cambia de tipo de documento , vuelve a la entidad Y, se debe verificar su existencia como transferido
    para evitar registros duplicados

    :param objeto: objeto transferible
    :param tipo_objeto: tipo del objeto transferible
    :return:
    """
    if tipo_objeto == 'Deportista':
        try:
           obj = Deportista.objects.get(identificacion=objeto.identificacion)
        except:
            posibilidades = Deportista.objects.filter(nombres=objeto.nombres, apellidos=objeto.apellidos).exclude(tipo_id=objeto.tipo_id)
            if len(posibilidades) == 0:
                return False,None
            else:
                return True,posibilidades
    return False,None

@login_required
def cancelar_transferencia(request,id_objeto,tipo_objeto):
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

    objeto = ''
    obj_trans = None
    if tipo_objeto=='1':
        objeto = 'Deportista'
        redir = 'deportista_listar'
        try:
            obj_trans = Deportista.objects.get(id=id_objeto)
        except:
            messages.error(request,'Error: No se puede procesar la solicitud, Deportista no existe')
            return redirect(redir)
    elif tipo_objeto=='2':
        objeto='PersonalApoyo'
        redir='personal_apoyo_listar'
        try:
            entre = PersonalApoyo.objects.get(id=id_objeto)
            entre.estado = 0
            entre.save()
        except:
            messages.error(request,'Error: No se puede procesar la solicitud, PersonalApoyo no existe')
            return redirect(redir)
    elif tipo_objeto=='3':
        objeto='Escenario'
        redir='listar_escenarios'
        try:
            obj_trans = Escenario.objects.get(id=id_objeto)
        except:
            messages.error(request,'Error: No se puede procesar la solicitud, Escenario no existe')
            return redirect(redir)

    obj_trans.estado = 0
    obj_trans.save()
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