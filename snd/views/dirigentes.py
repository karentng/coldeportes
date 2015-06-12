from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from formtools.wizard.views import *
from snd.formularios.dirigentes  import *
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings


def guardar_identificacion(wizard, dirigente_form):
    """
    Junio 12 / 2015
    Autor: Cristian Ríos
    
    Guarda la identificación del Dirigente

    Obtengo el formulario de identificación del Dirigente completo, le asigno la entidad que lo creo, lo guardo y lo retorno

    :param wizard:   Wizard que se despliega
    :type wizard:    NamedUrlSessionWizardView
    :param dirigente_form: Formulario de identificación
    :type dirigente_form:  DirigentesForm
    :returns:        Retorna el Dirigente
    :rtype:          Dirigente
    """

    dirigente = dirigente_form.save(commit=False)
    dirigente.entidad = wizard.request.tenant  
    dirigente.save()

    return dirigente

def guardar_formulario(wizard, dirigente, form):
    """
    Junio 12 / 2015
    Autor: Cristian Ríos
    
    Asocia (guarda) la información propia del dirigente (Funciones)

    Obtengo el formulario de información del Dirigente completo, le asigno el Dirigente al que corresponde y lo guardo

    :param wizard:   Wizard que se despliega
    :type wizard:    DirigenteWizard
    :param dirigente:   Dirigente
    :type centro:    Dirigente
    :param form:     Formularios de información del Dirigente
    :type form:      Puede ser: DirigentesFuncionesForm
    :returns:        No hay retorno
    :rtype:          None
    """
    formulario = form.save(commit=False)
    formulario.centro = dirigente
    form.save()

class DirigenteWizard(NamedUrlSessionWizardView):

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    template_name = 'dirigentes/nuevo.html'

    def done(self, form_list, form_dict, **kwargs):
        """
        Junio 12 / 2015
        Autor: Cristian Ríos
        
        Guarda toda la información del Dirigente que se registró

        Obtengo los formularios validados y los guardo.

        :param self:        Wizard
        :type self:         DirigenteWizard
        :param form_list:   Lista de formularios
        :type form_list:    ValuesView
        :param form_dict:   Formularios registrados
        :type form_dict:    OrderedDict
        """

        dirigente = guardar_identificacion(self, form_dict['Identificacion'])
        guardar_formulario(self, dirigente, form_dict['Funciones'])

        messages.success(self.request, "Dirigente registrado correctamente.")

        return redirect('dirigentes_listar')#<PENDIENTE>cambiar a listar dirigentes


@login_required
def listarDirigentes(request):
    return HttpResponse("Hola Dirigentes Lista")