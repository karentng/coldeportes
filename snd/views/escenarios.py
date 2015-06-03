from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import os
from snd.formularios.escenarios  import *
from snd.models import *
from entidades.models import *


"""
Autor: Karent Narvaez Grisales
Conjunto de Templates pasados al wizard según el paso actual del wizard
"""
TEMPLATES = {
             "Identificacion": 'escenarios/step_0_template.html',
             "Caracterizacion": 'escenarios/step_0_template.html',
             "Horarios": 'escenarios/horarios.html', 
             "Datos Historicos": 'escenarios/horarios.html', 
             "Fotos": 'escenarios/step_0_template.html', 
             "Videos": 'escenarios/step_0_template.html', 
             "Contacto": 'escenarios/horarios.html'}
"""
Autor: Karent Narvaez Grisales
Conjunto de formularios pasados al wizard según el paso actual del wizard
"""
FORMS = [ 
         ("Identificacion", IdentificacionForm),
         ("Caracterizacion", CaracterizacionForm),
         ("Horarios", HorariosDisponibleForm), 
         ("Datos Historicos", DatoHistoricoForm), 
         ("Fotos", FotoEscenarioForm), 
         ("Videos", VideoEscenarioForm), 
         ("Contacto", ContactoForm)]


def guardar_identificacion(wizard, escenario_form):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez
    
    Guarda el primer paso del wizard de los datos de identificación del escenario

    Se asigna el tenant que realiza la petición como la entidad responsable del escenario y se guarda el escenario
    :param wizard:     Wizard
    :type wizard:      SessionWizardView
    :param escenario:   Escenario
    :type escenario:    Escenario
    :returns:        Arreglo con los formularios información del escenario
    :rtype:          Escenario
    """
    escenario = escenario_form.save(commit=False)
    escenario.entidad = wizard.request.tenant   
    escenario.save()
    return escenario

def guardar_formulario(escenario, form):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    Guardar un formulario de wizard

    Se asigna el escenario respectivo para asociar al formulario pasado como parámetro y se guardan las relaciones muchos a muchos

    :param escenario:   Escenario guardado previamente con el que se relaciona el formulario
    :type escenario:    Escenario
    :param form:   formulario
    :type form:    formulario
    """
    formulario = form.save(commit=False)
    formulario.escenario = escenario
    form.save()


class EscenarioWizard(SessionWizardView):

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media_escenarios'))
    
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    #template_name = 'escenarios/step_0_template.html'

    def done(self, form_list, form_dict, **kwargs):
        #[form.cleaned_data for form in form_list]
        
        escenario = guardar_identificacion(self, form_dict['Identificacion'])
        guardar_formulario( escenario, form_dict['Caracterizacion'])
        guardar_formulario( escenario, form_dict['Horarios'])
        guardar_formulario( escenario, form_dict['Datos Historicos'])
        guardar_formulario( escenario, form_dict['Contacto'])
        

        return render(self.request,'escenarios/finalizado_registro.html')

@login_required
def listarEscenarios(request):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    listar los escenarios del tenant respectivo

    Se obtienen los escenario que ha registrado el tenant que realiza la petición

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    escenarios = Escenario.objects.filter(entidad=request.tenant)
    return render(request, 'escenarios/escenarios_lista.html', {
        'escenarios': escenarios,
    })

@login_required
def desactivarEscenario(request, escenario_id):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    desactivar escenario

    Se obtienen el estado actual del escenario y se invierte.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    """
    escenario = Escenario.objects.get(id=escenario_id)
    estado_actual = escenario.activo
    escenario.activo = not(estado_actual)
    escenario.save()
    return redirect('listar_escenarios')


@login_required
def editar_identificacion(request, escenario_id):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    Editar un Escenario

    Se obtienen los formularios de información del escenario con los datos diligenciados y se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    """

    try:
        escenario = Escenario.objects.get(id=escenario_id)
    except Exception:
        return redirect('listar_escenarios')

    identificacion_form = IdentificacionForm( instance=escenario)

    if request.method == 'POST':

        identificacion_form = IdentificacionForm(request.POST, instance=escenario)

        if identificacion_form.is_valid():
            identificacion_form.save()
            return redirect('editar_caracterizacion', escenario_id)


    return render(request, 'escenarios/wizard/editar_escenario.html', {
        'titulo': 'Identificación del Escenario',
        'wizard_stage': 1,
        'form': identificacion_form,
    })

@login_required
def editar_caracterizacion(request, escenario_id):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    Editar Características del Escenario

    Se obtienen el formulario de las características del escenario con la información actual y se guardan las modificaciones, si hay.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    """

    try:
        caracteristicas = CaracterizacionEscenario.objects.get(escenario=escenario_id)
    except Exception:
        return redirect('listar_escenarios')

    caracterizacion_form = CaracterizacionForm(instance=caracteristicas)

    if request.method == 'POST':
        caracterizacion_form = CaracterizacionForm(request.POST, instance=caracteristicas)

        if caracterizacion_form.is_valid():
            caracterizacion_form.save()
            print ('hola46')
            return redirect('editar_horarios', escenario_id)


    return render(request, 'escenarios/wizard/editar_escenario.html', {
        'titulo': 'Caracterización del Escenario',
        'wizard_stage': 2,
        'form': caracterizacion_form,
    })


@login_required
def editar_historicos(request, escenario_id):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    Editar los datos históricos de un Escenario

    Se obtienen el formulario de los datos históricos y se muestran los datos actualmente añadidos al escenario
    y si hay modificaciones se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    """

    try:
        historicos = DatoHistorico.objects.filter(escenario=escenario_id)
    except Exception:
        return redirect('listar_escenarios')

    historico_form = DatoHistoricoForm()

    if request.method == 'POST':
        historico_form = DatoHistoricoForm(request.POST)

        if historico_form.is_valid():
            historico_nuevo = historico_form.save(commit=False)
            historico_nuevo.escenario = Escenario.objects.get(id=escenario_id)
            historico_nuevo.save()
            return redirect('editar_historicos', escenario_id)


    return render(request, 'escenarios/wizard/editar_escenario_historicos.html', {
        'titulo': 'Datos Históricos del Escenario',
        'wizard_stage': 4,
        'form': historico_form,
        'historicos': historicos,
        'escenario_id': escenario_id
    })

@login_required
def editar_horarios(request, escenario_id):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    Editar los horarios de un Escenario

    Se obtienen el formulario de los horarios y se muestran los horarios actualmente añadidos al escenario
    y si hay modificaciones se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    """

    try:
        horarios = HorarioDisponibilidad.objects.filter(escenario=escenario_id)
    except Exception:
        return redirect('listar_escenarios')

    horarios_form = HorariosDisponibleForm()

    if request.method == 'POST':
        horarios_form = HorariosDisponibleForm(request.POST)

        if horarios_form.is_valid():
            horario_nuevo = horarios_form.save(commit=False)
            horario_nuevo.escenario = Escenario.objects.get(id=escenario_id)
            horario_nuevo.save()
            return redirect('editar_horarios', escenario_id)


    return render(request, 'escenarios/wizard/editar_escenario_grid.html', {
        'titulo': 'Horarios de Disponibildad del Escenario',
        'wizard_stage': 3,
        'form': horarios_form,
        'horarios': horarios,
        'escenario_id': escenario_id
    })

@login_required
def editar_fotos(request, escenario_id):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    Editar las fotos de un Escenario

    Se obtienen el formulario para subir fotos y se muestran las que actualmente hay añadidos al escenario
    y si hay modificaciones se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    """

    try:
        fotos = Foto.objects.filter(escenario=escenario_id)
    except Exception:
        return redirect('listar_escenarios')

    fotos_form = FotoEscenarioForm()

    if request.method == 'POST':
        fotos_form = FotoEscenarioForm(request.POST)

        if fotos_form.is_valid():
            foto_nueva = fotos_form.save(commit=False)
            foto_nueva.escenario = Escenario.objects.get(id=escenario_id)
            foto_nueva.save()
            return redirect('editar_fotos', escenario_id)


    return render(request, 'escenarios/wizard/editar_escenario_fotos.html', {
        'titulo': 'Fotos del Escenario',
        'wizard_stage': 5,
        'form': fotos_form,
        'fotos': fotos,
        'escenario_id': escenario_id
    })


@login_required
def editar_contactos(request, escenario_id):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    Editar los contactos de un Escenario

    Se obtienen el formulario para subir contactos y se muestran los que actualmente hay añadidos al escenario
    y si hay modificaciones se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    """

    try:
        contactos = Contacto.objects.filter(escenario=escenario_id)
    except Exception:
        return redirect('listar_escenarios')

    contactos_form = ContactoForm()

    if request.method == 'POST':
        contactos_form = ContactoForm(request.POST)

        if contactos_form.is_valid():
            contacto_nuevo = contactos_form.save(commit=False)
            contacto_nuevo.escenario = Escenario.objects.get(id=escenario_id)
            contacto_nuevo.save()
            return redirect('editar_contactos', escenario_id)


    return render(request, 'escenarios/wizard/editar_escenario_contactos.html', {
        'titulo': 'Contactos del Escenario',
        'wizard_stage': 7,
        'form': contactos_form,
        'contactos': contactos,
        'escenario_id': escenario_id
    })
    
@login_required
def editar_videos(request, escenario_id):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    Editar los videos de un Escenario

    Se obtienen el formulario para subir videos y se muestran loss que actualmente hay añadidos al escenario
    y si hay modificaciones se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    """

    try:
        videos = Video.objects.filter(escenario=escenario_id)
    except Exception:
        return redirect('listar_escenarios')

    videos_form = VideoEscenarioForm()

    if request.method == 'POST':
        videos_form = VideosEscenarioForm(request.POST)

        if videos_form.is_valid():
            video_nuevo = videos_form.save(commit=False)
            video_nuevo.escenario = Escenario.objects.get(id=escenario_id)
            video_nuevo.save()
            return redirect('editar_videos', escenario_id)


    return render(request, 'escenarios/wizard/editar_escenario_videos.html', {
        'titulo': 'Videos del Escenario',
        'wizard_stage': 6,
        'form': videos_form,
        'videos': videos,
        'escenario_id': escenario_id
    })


@login_required
def eliminar_horario(request, escenario_id, horario_id):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    Eliminar horario

    Se obtienen el horario de la base de datos y se elimina

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    """

    try:
        horario = HorarioDisponibilidad.objects.get(id=horario_id, escenario=escenario_id)
        horario.delete()
        return redirect('editar_horarios', escenario_id)

    except Exception:
        return redirect('editar_horarios', escenario_id)


@login_required
def eliminar_historico(request, escenario_id, historico_id):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    Eliminar histórico

    Se obtienen el dato histórico de la base de datos y se elimina

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    :param historico_id:   Identificador del dato historico
    :type historico_id:    String
    """

    try:
        historico = DatoHistorico.objects.get(id=historico_id, escenario=escenario_id)
        historico.delete()
        return redirect('editar_historicos', escenario_id)

    except Exception:
        return redirect('editar_historicos', escenario_id)

@login_required
def eliminar_foto(request, escenario_id, foto_id):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    Eliminar foto

    Se obtienen la foto de la base de datos y se elimina

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    :param foto_id:   Identificador de la foto
    :type foto_id:    String
    """

    try:
        foto = Foto.objects.get(id=foto_id, escenario=escenario_id)
        foto.delete()
        return redirect('editar_fotos', escenario_id)
    except Exception:
        return redirect('editar_fotos', escenario_id)

@login_required
def eliminar_video(request, escenario_id, video_id):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    Eliminar foto

    Se obtienen el video de la base de datos y se elimina

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    :param video_id:   Identificador del video
    :type video_id:    String
    """

    try:
        video = Video.objects.get(id=video_id, escenario=escenario_id)
        video.delete()
        return redirect('editar_videos', escenario_id)
    except Exception:
        return redirect('editar_videos', escenario_id)

@login_required
def eliminar_contacto(request, escenario_id, contacto_id):
    """
    Mayo 30 / 2015
    Autor: Karent Narvaez Grisales
    
    Eliminar contacto

    Se obtienen el contacto de la base de datos y se elimina

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    :param contacto_id:   Identificador del contacto
    :type contacto_id:    String
    """

    try:
        contacto = Contacto.objects.get(id=contacto_id, escenario=escenario_id)
        contacto.delete()
        return redirect('editar_contactos', escenario_id)
    except Exception:
        return redirect('editar_contactos', escenario_id)


