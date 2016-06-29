from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from snd.models import *
from directorio.forms import *
from directorio.models import *
from directorio.inicializacion_vistas_directorio import crear_vistas

    
def buscar_contenido(texto, listado_resultados):

    listado_resultados += list(EscenarioView.objects.filter(nombre__icontains=texto).distinct('id'))
    listado_resultados += list(CAFView.objects.filter(nombre__icontains=texto).distinct('id'))
    listado_resultados += list(DeportistaView.objects.filter(nombre__icontains=texto).distinct('id'))
    listado_resultados += list(PersonalApoyoView.objects.filter(nombre__icontains=texto).distinct('id'))
    listado_resultados += list(DirigenteView.objects.filter(nombre__icontains=texto).distinct('id'))
    listado_resultados += list(CajaCompensacionView.objects.filter(nombre__icontains=texto).distinct('id'))    
    return listado_resultados


def buscar_contenido_ciudad(texto, ciudades, listado_resultados):

    listado_resultados += list(EscenarioView.objects.filter(nombre__icontains=texto, ciudad__in = ciudades).distinct('id'))
    listado_resultados += list(CAFView.objects.filter(nombre__icontains=texto, ciudad__in = ciudades).distinct('id'))
    listado_resultados += list(DeportistaView.objects.filter(nombre__icontains=texto, ciudad_residencia__in = ciudades).distinct('id'))
    listado_resultados += list(PersonalApoyoView.objects.filter(nombre__icontains=texto, ciudad__in = ciudades).distinct('id'))
    listado_resultados += list(DirigenteView.objects.filter(nombre__icontains=texto, ciudad__in = ciudades).distinct('id'))
    listado_resultados += list(CajaCompensacionView.objects.filter(nombre__icontains=texto, ciudad__in = ciudades).distinct('id'))
    return listado_resultados
    

def buscar_contenido_actor(texto, actor,listado_resultados):

    if actor=='ES':
        listado_resultados += list(EscenarioView.objects.filter(nombre__icontains=texto).distinct('id'))
    elif actor=='CA':
        listado_resultados += list(CAFView.objects.filter(nombre__icontains=texto).distinct('id'))
    elif actor=='DE':
        listado_resultados += list(DeportistaView.objects.filter(nombre__icontains=texto).distinct('id'))
    elif actor=='DI':
        listado_resultados += list(DirigenteView.objects.filter(nombre__icontains=texto).distinct('id'))
    elif actor=='PA':
        listado_resultados += list(PersonalApoyoView.objects.filter(nombre__icontains=texto).distinct('id'))
    elif actor=='CF':
        listado_resultados += list(CajaCompensacionView.objects.filter(nombre__icontains=texto).distinct('id'))
    return listado_resultados


def buscar_contenido_actor_ciudad(actor, ciudades, texto, listado_resultados):

    if actor=='ES':
        listado_resultados += list(EscenarioView.objects.filter(nombre__icontains=texto, ciudad__in = ciudades).distinct('id'))
    elif actor=='CA':
        listado_resultados += list(CAFView.objects.filter(nombre__icontains=texto, ciudad__in = ciudades).distinct('id'))
    elif actor=='DE':
        listado_resultados += list(DeportistaView.objects.filter(nombre__icontains=texto, ciudad_residencia__in = ciudades).distinct('id'))
    elif actor=='DI':
        listado_resultados += list(DirigenteView.objects.filter(nombre__icontains=texto, ciudad__in = ciudades).distinct('id'))
    elif actor=='PA':
        listado_resultados += list(PersonalApoyoView.objects.filter(nombre__icontains=texto, ciudad__in = ciudades).distinct('id'))
    elif actor=='CF':
        listado_resultados += list(CajaCompensacionView.objects.filter(nombre__icontains=texto, ciudad__in = ciudades).distinct('id'))
    return listado_resultados


def agregar_grupo(resultados):
    
    for objeto in resultados:
        objeto.grupo = objeto.__class__.__name__


def directorio_buscar(request):
    """
    Julio 22 / 2015
    Autor: Karent Narvaez Grisales
    
    realizar búsqueda de los diferentes criterios para un contacto en el directorio.

    Se obtienen los resultados que coincidan con la búsqueda que ha registrado el tenant que realiza la petición

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    #inicializado formulario de búsqueda
    form = DirectorioBusquedaForm()
    #inicialización de variable resultados
    listado_resultados = []
    mensaje = 'No hay resultados para la búsqueda.'

    if request.method == 'POST':        
        form = DirectorioBusquedaForm(request.POST)

        if form.is_valid():
            ciudades = request.POST.getlist('ciudad') or None
            categoria = request.POST.getlist('actor') or None
            texto = request.POST.get('texto_a_buscar') or ''

            #Si intenta búscar sin filtros
            if categoria == None and texto == '' and ciudades == None:
                mensaje = 'Por favor ingrese un criterio de búsqueda.'
            #Si busca solo con texto
            elif categoria == None and ciudades == None:
                listado_resultados = buscar_contenido(texto, listado_resultados)
            # Si busca solo con ciudades
            elif categoria == None and ciudades != None:
                listado_resultados = buscar_contenido_ciudad(texto, ciudades, listado_resultados)
            #Si busca sólo con categoría
            elif categoria != None and ciudades == None:
                for actor in categoria :                    
                    listado_resultados = buscar_contenido_actor(texto, actor, listado_resultados)
            #Si busca por categorías y con ciudades
            else:
                for actor in categoria :
                    listado_resultados = buscar_contenido_actor_ciudad(actor, ciudades, texto, listado_resultados)
            
            # a cada objeto se agrega de que grupo es para dividirlos en el template
            agregar_grupo(listado_resultados)

    return render(request, 'directorio_buscar.html', {
        'form': form,
        'listado_resultados': listado_resultados,
        'mensaje': mensaje,
    })

#@login_required
#def ver_detalles(request, id, grupo):