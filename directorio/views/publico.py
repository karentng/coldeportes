from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from directorio.forms import *
from directorio.models import *
from snd.models import *
from django.db import connection
from directorio.inicializacion_vistas_directorio import *

    
def buscar_contenido(texto, listado_resultados):
    listado_resultados += list(EscenarioView.objects.filter(nombre__icontains=texto).distinct('id'))
    listado_resultados += list(CAFView.objects.filter(nombre__icontains=texto).distinct('id'))
    listado_resultados += list(DeportistaView.objects.filter(nombre__icontains=texto).distinct('id'))
    listado_resultados += list(PersonalApoyoView.objects.filter(nombre__icontains=texto).distinct('id'))
    listado_resultados += list(DirigenteView.objects.filter(nombre__icontains=texto).distinct('id'))
    listado_resultados += list(CajaCompensacionView.objects.filter(nombre__icontains=texto).distinct('id'))
    
    return listado_resultados

def buscar_contenido_ciudad(texto, ciudad, listado_resultados):
    listado_resultados += list(EscenarioView.objects.filter(nombre__icontains=texto, ciudad=ciudad).distinct('id'))
    listado_resultados += list(CAFView.objects.filter(nombre__icontains=texto, ciudad=ciudad).distinct('id'))
    listado_resultados += list(DeportistaView.objects.filter(nombre__icontains=texto, ciudad_residencia=ciudad).distinct('id'))
    listado_resultados += list(PersonalApoyoView.objects.filter(nombre__icontains=texto, ciudad=ciudad).distinct('id'))
    listado_resultados += list(DirigenteView.objects.filter(nombre__icontains=texto, ciudad=ciudad).distinct('id'))
    listado_resultados += list(CajaCompensacionView.objects.filter(nombre__icontains=texto).distinct('id'))

    return listado_resultados
    
def buscar_contenido_actor(texto, actor, listado_resultados):
    if actor == 'ES':
        listado_resultados += list(EscenarioView.objects.filter(nombre__icontains=texto).distinct('id'))
    elif actor == 'CA':
        listado_resultados += list(CAFView.objects.filter(nombre__icontains=texto).distinct('id'))
    elif actor == 'DE':
        listado_resultados += list(DeportistaView.objects.filter(nombre__icontains=texto).distinct('id'))
    elif actor == 'DI':
        listado_resultados += list(DirigenteView.objects.filter(nombre__icontains=texto).distinct('id'))
    elif actor == 'PA':
        listado_resultados += list(PersonalApoyoView.objects.filter(nombre__icontains=texto).distinct('id'))
    elif actor == 'CF':
        listado_resultados += list(CajaCompensacionView.objects.filter(nombre__icontains=texto).distinct('id'))

    return listado_resultados

def buscar_contenido_actor_ciudad(actor, ciudad, texto, listado_resultados):
    if actor == 'ES':
        listado_resultados += list(EscenarioView.objects.filter(nombre__icontains=texto, ciudad=ciudad).distinct('id'))
    elif actor == 'CA':
        listado_resultados += list(CAFView.objects.filter(nombre__icontains=texto, ciudad=ciudad).distinct('id'))
    elif actor == 'DE':
        listado_resultados += list(DeportistaView.objects.filter(nombre__icontains=texto, ciudad_residencia=ciudad).distinct('id'))
    elif actor == 'DI':
        listado_resultados += list(DirigenteView.objects.filter(nombre__icontains=texto, ciudad=ciudad).distinct('id'))
    elif actor == 'PA':
        listado_resultados += list(PersonalApoyoView.objects.filter(nombre__icontains=texto, ciudad=ciudad).distinct('id'))
    elif actor == 'CF':
        listado_resultados += list(CajaCompensacionView.objects.filter(nombre__icontains=texto).distinct('id'))

    return listado_resultados

def agregar_grupo(resultados):
    for resultado in resultados:
        for objeto in resultado:
            objeto.grupo=objeto.__class__.__name__

def buscar_resultados(ciudades, categoria, texto):
    listado_resultados = []


    #Si busca sin filtros
    if categoria == None and ciudades == None and texto == '':
        listado_resultados += list('N')#Se retorna un string como primer elemento si se intetna realizar búsquda sin filtros
    #Si busca solo con texto
    elif categoria == None and ciudades == None:
        listado_resultados = buscar_contenido(texto, listado_resultados)
    # Si busca solo con ciudades
    elif categoria == None and ciudades != None:
        for ciudad in ciudades:
            listado_resultados = buscar_contenido_ciudad(texto, ciudad, listado_resultados)
    #Si busca sólo con categoría
    elif categoria != None and ciudades == None:
        for actor in categoria :                  
            listado_resultados = buscar_contenido_actor(texto, actor, listado_resultados)

    #Si búsca por categorías y con ciudades
    else:
        for ciudad in ciudades:
            for actor in categoria :
                listado_resultados = buscar_contenido_actor_ciudad(actor, ciudad, texto, listado_resultados)
    
       
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

            entidades = Entidad.objects.exclude(schema_name='public')

            for entidad in entidades:
                connection.set_tenant(entidad)             

                checkear_inicializacion_directorio()
                listado_resultados.append(buscar_resultados(ciudades, categoria, texto))
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