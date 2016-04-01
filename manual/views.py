from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from coldeportes.utilities import all_permission_required
from manual.models import Articulo
from manual.forms import ArticuloForm
from entidades.models import TIPOS

# Create your views here.
@login_required
@all_permission_required('manual.add_articulo')
def nueva_entrada(request):
    """
    Enero 28 / 2016
    Autor: Karent Narvaez Grisales
    
    registro de la información de un artículo en el manual de usuario.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    articulo_form = ArticuloForm( )

    if request.method == 'POST':

        articulo_form = ArticuloForm(request.POST, request.FILES)

        if articulo_form.is_valid():
            articulo_form.save()
            messages.success(request, ("Artículo registrado correctamente."))
            
            return redirect('nueva_entrada_manual')


    return render(request, 'nueva_entrada.html', {
        'form': articulo_form,
    })

@login_required
@all_permission_required('manual.add_articulo')
def editar_articulo(request, articulo_id):
    """
    Enero 28 / 2016
    Autor: Karent Narvaez Grisales
    
    Edición de la información de un artículo en el manual de usuario.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param articulo_id: Identificador del artículo
    :type articulo_id: String
    """
    articulo_edicion =  Articulo.objects.get(id=articulo_id)
    articulo_form = ArticuloForm(instance=articulo_edicion)
    print('alskalskas')
    if request.method == 'POST':

        articulo_form = ArticuloForm(request.POST, request.FILES, instance=articulo_edicion)

        if articulo_form.is_valid():
            articulo_form.save()
            messages.success(request, ("Artículo registrado correctamente."))
            
            return redirect('listar_manual')


    return render(request, 'nueva_entrada.html', {
        'form': articulo_form,
        'edicion': True
    })

@login_required
def listar_articulo(request, articulo_id):
    """
    Enero 28 / 2016
    Autor: Karent Narvaez Grisales
    
    Ver artículos de manual de usuario.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    articulo = get_object_or_404(Articulo,id=articulo_id)

    items_manual = Articulo.MODULOS
    articulos = Articulo.objects.all()
    entidades = TIPOS


    mensaje = "No hay artísulos registrados."

    return render(request, 'listar_articulo.html', {
        'articulos': articulos,
        'mensaje': mensaje,
        'items': items_manual,
        'articulo': articulo,
        'entidades': entidades

    })


def encontrar_articulos_tenant(tenant_actual):
    #Todos los artículos
    if tenant_actual.schema_name=='public':
        articulos = Articulo.objects.all()
    else:
        articulos = Articulo.objects.filter(entidad=tenant_actual.tipo)

    return articulos


def filtrar_entidades(entidades, tenant_actual):
    if tenant_actual.schema_name=='public':
        return entidades
    else:
        entidades = [entidades[tenant_actual.tipo-1]]
        return entidades

@login_required
def listar(request):
    """
    Febrero 9 / 2016
    Autor: Karent Narvaez Grisales
    
    Listar tree list para manual sin ningún manual en especial seleccionado.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    items_manual = Articulo.MODULOS
    tenant_actual = request.tenant
    entidades = TIPOS
    mensaje = "No hay artísulos registrados."

    
    articulos = encontrar_articulos_tenant(tenant_actual)
    entidades = filtrar_entidades(entidades, tenant_actual)

    print(entidades)

    return render(request, 'tree_list.html', {
        'articulos': articulos,
        'mensaje': mensaje,
        'items': items_manual,
        'entidades': entidades

    })