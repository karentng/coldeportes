from django.db import connection
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from snd.models import *
from directorio.forms import *
from directorio.models import EscenarioPublicView, CAFPublicView, DeportistaPublicView, PersonalApoyoPublicView, DirigentePublicView, CajaCompensacionPublicView

    
def buscar_contenido(texto):
    listado_resultados = []
    listado_resultados += list(EscenarioPublicView.objects.filter(contenido__icontains=texto).distinct('id', 'entidad'))
    listado_resultados += list(CAFPublicView.objects.filter(contenido__icontains=texto).distinct('id', 'entidad'))
    listado_resultados += list(DeportistaPublicView.objects.filter(contenido__icontains=texto).distinct('id', 'entidad'))
    listado_resultados += list(PersonalApoyoPublicView.objects.filter(contenido__icontains=texto).distinct('id', 'entidad'))
    listado_resultados += list(DirigentePublicView.objects.filter(contenido__icontains=texto).distinct('id', 'entidad'))
    listado_resultados += list(CajaCompensacionPublicView.objects.filter(contenido__icontains=texto).distinct('id', 'entidad'))    
    return listado_resultados


def buscar_contenido_ciudad(texto, ciudades):
    listado_resultados = []    
    listado_resultados += list(EscenarioPublicView.objects.filter(contenido__icontains=texto, ciudad__in=ciudades).distinct('id', 'entidad'))
    listado_resultados += list(CAFPublicView.objects.filter(contenido__icontains=texto, ciudad__in=ciudades).distinct('id', 'entidad'))
    listado_resultados += list(DeportistaPublicView.objects.filter(contenido__icontains=texto, ciudad_residencia__in=ciudades).distinct('id', 'entidad'))
    listado_resultados += list(PersonalApoyoPublicView.objects.filter(contenido__icontains=texto, ciudad__in=ciudades).distinct('id', 'entidad'))
    listado_resultados += list(DirigentePublicView.objects.filter(contenido__icontains=texto, ciudad__in=ciudades).distinct('id', 'entidad'))
    listado_resultados += list(CajaCompensacionPublicView.objects.filter(contenido__icontains=texto).distinct('id', 'entidad'))
    return listado_resultados
    

def buscar_contenido_actor(texto, actor):
    listado_resultados = []
    if actor == 'ES':
        listado_resultados += list(EscenarioPublicView.objects.filter(contenido__icontains=texto).distinct('id', 'entidad'))
    elif actor == 'CA':
        listado_resultados += list(CAFPublicView.objects.filter(contenido__icontains=texto).distinct('id', 'entidad'))
    elif actor == 'DE':
        listado_resultados += list(DeportistaPublicView.objects.filter(contenido__icontains=texto).distinct('id', 'entidad'))
    elif actor == 'DI':
        listado_resultados += list(DirigentePublicView.objects.filter(nombre__icontains=texto).distinct('id', 'entidad'))
    elif actor == 'PA':
        listado_resultados += list(PersonalApoyoPublicView.objects.filter(contenido__icontains=texto).distinct('id', 'entidad'))
    elif actor == 'CF':
        listado_resultados += list(CajaCompensacionPublicView.objects.filter(contenido__icontains=texto).distinct('id', 'entidad'))
    return listado_resultados


def buscar_contenido_actor_ciudad(actor, ciudades, texto):
    listado_resultados = []
    if actor == 'ES':
        listado_resultados += list(EscenarioPublicView.objects.filter(contenido__icontains=texto, ciudad__in=ciudades).distinct('id', 'entidad'))
    elif actor == 'CA':
        listado_resultados += list(CAFPublicView.objects.filter(contenido__icontains=texto, ciudad__in=ciudades).distinct('id', 'entidad'))
    elif actor == 'DE':
        listado_resultados += list(DeportistaPublicView.objects.filter(contenido__icontains=texto, ciudad_residencia__in=ciudades).distinct('id', 'entidad'))
    elif actor == 'DI':
        listado_resultados += list(DirigentePublicView.objects.filter(contenido__icontains=texto, ciudad__in=ciudades).distinct('id', 'entidad'))
    elif actor == 'PA':
        listado_resultados += list(PersonalApoyoPublicView.objects.filter(contenido__icontains=texto, ciudad__in=ciudades).distinct('id', 'entidad'))
    elif actor == 'CF':
        listado_resultados += list(CajaCompensacionPublicView.objects.filter(contenido__icontains=texto).distinct('id', 'entidad'))
    return listado_resultados


def agregar_grupo(resultados):

    for resultado in resultados:
        if resultado.__class__.__name__ == 'DeportistaPublicView':
            resultado.grupo = 'DeportistaView'
        elif resultado.__class__.__name__ == 'DirigentePublicView':
            resultado.grupo = 'DirigenteView'
        elif resultado.__class__.__name__ == 'PersonalApoyoPublicView':
            resultado.grupo = 'PersonalApoyoView'
        elif resultado.__class__.__name__ == 'CAFPublicView':
            resultado.grupo = 'CAFView'
        elif resultado.__class__.__name__ == 'EscenarioPublicView':
            resultado.grupo = 'EscenarioView'
        elif resultado.__class__.__name__ == 'CajaCompensacionPublicView':
            resultado.grupo = 'CajaView'


def buscar_resultados(ciudades, categoria, texto):

    listado_resultados = []
    #Si busca sin filtros
    if categoria == None and ciudades == None and texto == '':
        listado_resultados = list('N')#Se retorna un string como primer elemento si se intenta realizar búsquda sin filtros
    #Si busca solo con texto
    elif categoria == None and ciudades == None:
        listado_resultados = buscar_contenido(texto)
    # Si busca solo con ciudades
    elif categoria == None and ciudades != None:
        listado_resultados = buscar_contenido_ciudad(texto, ciudades)
    #Si busca sólo con categoría
    elif categoria != None and ciudades == None:
        for actor in categoria :                  
            listado_resultados = buscar_contenido_actor(texto, actor)
    #Si busca por categorías y con ciudades
    else:
        for actor in categoria :
            listado_resultados = buscar_contenido_actor_ciudad(actor, ciudades, texto) 
    return listado_resultados


def directorio_publico_buscar(request):
    """
    Agosto 5 / 2015
    Autor: Karent Narvaez Grisales
    
    realizar búsqueda de los diferentes criterios para un contacto en el directorio en todos los tenants.

    Se obtienen los resultados que coinciden con la búsqueda en todos los tenants.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    #Definiendo tenant actual
    tenant_actual = connection.tenant  
    #inicializado formulario de búsqueda
    form = DirectorioBusquedaForm()
    #inicialización de variable resultados
    listado_resultados =[]
    mensaje = 'No hay resultados para la búsqueda.'

    if request.method == 'POST':        
        form = DirectorioBusquedaForm(request.POST)

        if form.is_valid():
            ciudades = request.POST.getlist('ciudad') or None
            categoria = request.POST.getlist('actor') or None
            texto = request.POST.get('texto_a_buscar') or ''
            #entidades = Entidad.objects.exclude(schema_name='public')

            #for entidad in entidades:
            #connection.set_tenant(entidad) 
            listado_resultados = buscar_resultados(ciudades, categoria, texto)
            # a cada objeto se agrega de que grupo es para dividirlos en el template
            try:
                if isinstance(listado_resultados[0][0], str):# se verifica si el primer elemento de los resultados es un string según la validación solo se da cuando se intentó hacer búsqueda sin filtros
                    mensaje = 'Por favor ingrese un criterio de búsqueda.'
                    listado_resultados = []
                else:
                    agregar_grupo(listado_resultados)
            except:
                agregar_grupo(listado_resultados)                
    #se configura de nuevo el tenant inicial
    connection.set_tenant(tenant_actual)

    return render(request, 'directorio_buscar.html', {
        'form': form,
        'listado_resultados': listado_resultados,
        'mensaje': mensaje,
    })