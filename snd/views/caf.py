from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from formtools.wizard.views import *
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from snd.models import *
from entidades.models import *
from snd.formularios.caf import *

def guardar_identificacion(wizard, caf_form):
    """
    Mayo 26 / 2015
    Autor: Andrés Serna
    
    Guarda la identificación del centro de acondicionamiento físico

    Obtengo el formulario de identificación de CAF completo, le asigno la entidad que lo creo, lo guardo y lo retorno

    :param wizard:   Wizard que se despliega
    :type wizard:    NamedUrlSessionWizardView
    :param caf_form: Formulario de identificación
    :type caf_form:  CentroAcondicionamientoForm
    :returns:        Retorna el CAF
    :rtype:          CentroAcondicionamiento
    """

    centro = caf_form.save(commit=False)
    centro.entidad = wizard.request.tenant  
    centro.save()

    return centro

def guardar_formulario(wizard, centro, form):
    """
    Mayo 26 / 2015
    Autor: Andrés Serna
    
    Asocia (guarda) la información propia del CAF (Costos, Servicios, Otros)

    Obtengo el formulario de información de CAF completo, le asigno el CAF al que corresponde y lo guardo

    :param wizard:   Wizard que se despliega
    :type wizard:    CentroAcondicionamientoWizard
    :param centro:   Centro de acondicionamiento físico
    :type centro:    CentroAcondicionamiento
    :param form:     Formularios de información del CAF
    :type form:      Puede ser: CACostoUsoForm, CAServiciosForm o CAOtrosForm
    :returns:        No hay retorno
    :rtype:          None
    """
    formulario = form.save(commit=False)
    formulario.centro = centro
    form.save()

class CentroAcondicionamientoWizard(NamedUrlSessionWizardView):

    template_name = 'cafs/nuevo.html'

    def done(self, form_list, form_dict, **kwargs):
        """
        Mayo 26 / 2015
        Autor: Andrés Serna
        
        Guarda toda la información del CAF que se registró

        Obtengo los formularios validados y los guardo.

        :param self:        Wizard
        :type self:         CentroAcondicionamientoWizard
        :param form_list:   Lista de formularios
        :type form_list:    ValuesView
        :param form_dict:   Formularios registrados
        :type form_dict:    OrderedDict
        """

        centro = guardar_identificacion(self, form_dict['Identificación'])
        guardar_formulario(self, centro, form_dict['Costos'])
        guardar_formulario(self, centro, form_dict['Servicios'])
        guardar_formulario(self, centro, form_dict['Otros'])
        
        return render(self.request,'cafs/finalizado_registro.html')

@login_required
def listarCAFS(request):
    """
    Mayo 26 / 2015
    Autor: Andrés Serna
    
    Despliega todos los CAF's registrados en la entidad

    Obtengo todos los CAF's y los envío al template como "cafs"

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """

    cafs = CentroAcondicionamiento.objects.all()
    return render(request, 'cafs/cafs_lista.html', {
        'cafs': cafs,
    })

@login_required
def desactivarCAF(request, idCAF):
    """
    Mayo 26 / 2015
    Autor: Andrés Serna
    
    Desactiva el CAF seleccionado

    Recupero el identificador del CAF seleccionado, lo obtengo de la base de datos, asigno la negación de su estado actual y lo guardo.

    :param wizard:   Wizard que se despliega
    :type wizard:    NamedUrlSessionWizardView
    :param idCAF:    Identificador del CAF seleccionado
    :type idCAF:     String
    """
    try:
        caf = CentroAcondicionamiento.objects.get(id=idCAF)
    except Exception:
        return redirect('listar_cafs')

    caf.activo = not(caf.activo)
    caf.save()
    
    return redirect('listar_cafs')

def traerFormularioCAF(centro, idForm, post=None):
    """
    Mayo 26 / 2015
    Autor: Andrés Serna
    
    Retorna el formulario elegido de acuerdo a idForm

    Obtengo la instancia del formulario elegido de acuerdo a idForm, se adiciona la información del POST si existe y se retorna.

    :param centro:   Centro de acondicionamiento físico
    :type centro:    CentroAcondicionamiento
    :param idForm:   Identificador que determina el formulario a retornar
    :type idForm:    Integer
    :param post:     Datos diligeciados de los formularios
    :type post:      QueryDict
    :returns:        Formulario información del CAF
    :rtype:          CentroAcondicionamientoForm, CACostoUsoForm, CAServiciosForm o CAOtrosForm
    """

    if idForm == 0:
        form = CentroAcondicionamientoForm(post, instance=centro)
    elif idForm == 1:
        costos = CACostoUso.objects.get(centro=centro)
        form = CACostoUsoForm(post, instance=costos)
    elif idForm == 2:
        servicios = CAServicios.objects.get(centro=centro)
        form = CAServiciosForm(post, instance=servicios)
    else:
        otros = CAOtros.objects.get(centro=centro)
        form = CAOtrosForm(post, instance=otros)

    return form

@login_required
def modificar(request, idCAF, idForm=0):

    """
    Mayo 26 / 2015
    Autor: Andrés Serna
    
    Modificar un CAF

    Se obtienen el formulario de información del CAF con los datos diligenciados y se guardan (si se ha realizado la petición POST válida).

    :param request:  Petición realizada
    :type request:   WSGIRequest
    :param idCAF:    Identificador del CAF
    :type idCAF:     String
    :param idForm:   Identificador que determina el formulario a retornar (por defecto 0)
    :type idForm:    String
    """

    try:
        centro = CentroAcondicionamiento.objects.get(id=idCAF)
        idForm = int(idForm)
        if idForm < 0 or idForm > 3:
            return redirect('listar_cafs')
    except Exception:
        return redirect('listar_cafs')

    form = traerFormularioCAF(centro, idForm)

    if request.method == 'POST':
        form = traerFormularioCAF(centro, idForm, request.POST)

        if form.is_valid():
            form.save()
            return redirect('modificar_caf', idCAF, idForm+1)

    return render(request, 'cafs/cafs_modificar.html', {
        'form': form,
        'idForm': idForm + 1,
        'idCAF': idCAF,
    })