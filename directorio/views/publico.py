from django.shortcuts import redirect, render
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from directorio.forms import *
from directorio.models import *
from snd.models import *
from django.db import connection

    
def buscar_contenido(texto, listado_resultados):
    listado_resultados.append(EscenarioView.objects.filter(contenido__icontains=texto).distinct('id'))
    listado_resultados.append(CAFView.objects.filter(contenido__icontains=texto).distinct('id'))
    listado_resultados.append(DeportistaView.objects.filter(contenido__icontains=texto).distinct('id'))
    listado_resultados.append(PersonalApoyoView.objects.filter(contenido__icontains=texto).distinct('id'))
    listado_resultados.append(DirigenteView.objects.filter(contenido__icontains=texto).distinct('id'))
    listado_resultados.append(CajaCompensacionView.objects.filter(contenido__icontains=texto).distinct('id'))
    
    return listado_resultados

def buscar_contenido_ciudad(texto, ciudad, listado_resultados):
    listado_resultados.append(EscenarioView.objects.filter(contenido__icontains=texto, ciudad=ciudad).distinct('id'))
    listado_resultados.append(CAFView.objects.filter(contenido__icontains=texto, ciudad=ciudad).distinct('id'))
    listado_resultados.append(DeportistaView.objects.filter(contenido__icontains=texto, ciudad_residencia=ciudad).distinct('id'))
    listado_resultados.append(PersonalApoyoView.objects.filter(contenido__icontains=texto, ciudad=ciudad).distinct('id'))
    listado_resultados.append(DirigenteView.objects.filter(contenido__icontains=texto, ciudad_residencia=ciudad).distinct('id'))
    listado_resultados.append(CajaCompensacionView.objects.filter(contenido__icontains=texto, ciudad=ciudad).distinct('id'))

    return listado_resultados
    
def buscar_contenido_actor(texto, actor,listado_resultados):
    if actor=='ES':
        listado_resultados.append(EscenarioView.objects.filter(contenido__icontains=texto).distinct('id'))
    elif actor=='CA':
        listado_resultados.append(CAFView.objects.filter(contenido__icontains=texto).distinct('id'))
    elif actor=='DE':
        listado_resultados.append(DeportistaView.objects.filter(contenido__icontains=texto).distinct('id'))
    elif actor=='DI':
        listado_resultados.append(DirigenteView.objects.filter(contenido__icontains=texto).distinct('id'))
    elif actor=='EN':
        listado_resultados.append(PersonalApoyoView.objects.filter(contenido__icontains=texto).distinct('id'))
    elif actor=='CF':
        listado_resultados.append(CajaCompensacionView.objects.filter(contenido__icontains=texto).distinct('id'))

    return listado_resultados

def buscar_contenido_actor_ciudad(actor, ciudad, texto, listado_resultados):
    if actor=='ES':
        listado_resultados.append(EscenarioView.objects.filter(contenido__icontains=texto, ciudad=ciudad).distinct('id'))
    elif actor=='CA':
        listado_resultados.append(CAFView.objects.filter(contenido__icontains=texto, ciudad=ciudad).distinct('id'))
    elif actor=='DE':
        listado_resultados.append(DeportistaView.objects.filter(contenido__icontains=texto, ciudad_residencia=ciudad).distinct('id'))
    elif actor=='DI':
        listado_resultados.append(DirigenteView.objects.filter(contenido__icontains=texto, ciudad_residencia=ciudad).distinct('id'))
    elif actor=='EN':
        listado_resultados.append(PersonalApoyoView.objects.filter(contenido__icontains=texto, ciudad=ciudad).distinct('id'))
    elif actor=='CF':
        listado_resultados.append(CajaCompensacionView.objects.filter(contenido__icontains=texto).distinct('id')) 

    return listado_resultados

def agregar_grupo(resultados):
    for resultado in resultados:
        for objeto in resultado:
            objeto.grupo=objeto.__class__.__name__


def buscar_resultados(ciudades, categoria, texto, listado_resultados):

    #Si busca solo con texto
    if categoria ==None and ciudades==None:
        listado_resultados = buscar_contenido(texto, listado_resultados)
    # Si busca solo con ciudades
    elif categoria ==None and ciudades!=None:
        for ciudad in ciudades:
            listado_resultados=buscar_contenido_ciudad(texto, ciudad, listado_resultados)
    #Si busca sólo con categoría
    elif categoria !=None and ciudades==None:
        for actor in categoria :                    
            listado_resultados = buscar_contenido_actor(texto, actor, listado_resultados)
    #Si búsca por categorías y con ciudades
    else:
        for ciudad in ciudades:
            for actor in categoria :
                listado_resultados = buscar_contenido_actor_ciudad(actor, ciudad, texto, listado_resultados)


@login_required
def directorio_buscar(request):
    """
    Agosto 5 / 2015
    Autor: Karent Narvaez Grisales
    
    realizar búsqueda de los diferentes criterios para un contacto en el directorio.

    Se obtienen los escenario que ha registrado el tenant que realiza la petición

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    
    #inicializado formulario de búsqueda
    form = DirectorioBusquedaForm()

    #inicialización de variable resultados
    listado_resultados =[]

    if request.method == 'POST':
        
        form = DirectorioBusquedaForm(request.POST)


        if form.is_valid():
            ciudades = request.POST.getlist('ciudad') or None
            categoria = request.POST.getlist('actor') or None
            texto = request.POST.get('texto_a_buscar') or ''

            entidades = Entidad.objects.all()
            tenant_actual = connection.tenant

            for entidad in entidades:
                connection.set_tenant(entidad)
                ContentType.objects.clear_cache()
                try:
                    listado_resultados = buscar_resultados(categoria, ciudades, text, listado_resultados)
                except Exception:
                    pass

            connection.set_tenant(tenant_actual)
            
            # a cada objeto se agrega de que grupo es para dividirlos en el template
            agregar_grupo(listado_resultados)

    print(listado_resultados)

    return render(request, 'directorio_buscar.html', {
        'form': form,
        'listado_resultados': listado_resultados,
    })