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
@all_permission_required('manual.add_articulo')
def eliminar_articulo(request, articulo_id):
    """
    Marzo 30 / 2016
    Autor: Karent Narvaez Grisales
    
    Eliminar un artículo en el manual de usuario.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param articulo_id: Identificador del artículo
    :type articulo_id: String
    """
    articulo = get_object_or_404(Articulo, id=articulo_id)
    articulo.delete()
    return redirect('listar_manual')


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
    entidades = TIPOS
    tenant_actual = request.tenant
    mensaje = "No hay artículos registrados."


    articulos = encontrar_articulos_tenant(tenant_actual)
    entidades = filtrar_entidades(entidades, tenant_actual)

    return render(request, 'listar_articulo.html', {
        'articulos': articulos,
        'mensaje': mensaje,
        'items': items_manual,
        'articulo': articulo,
        'entidades': entidades

    })



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
    items_manual_nueva = []
    abrir_tree = True
    entidades = TIPOS
    tenant_actual = request.tenant
    mensaje = "No hay artículos registrados."

    if tenant_actual.schema_name=='public':        
        items_manual_nueva = items_manual
        abrir_tree = False
    else: 
        for item in items_manual:
            if tenant_actual.actores.centros and item[0] == 'CF':
                items_manual_nueva += [item]
            elif tenant_actual.actores.cajas and item[0] == 'CC':
                items_manual_nueva += [item]
            elif tenant_actual.actores.centros_biomedicos and item[0] == 'CE':
                items_manual_nueva += [item]
            elif tenant_actual.actores.deportistas and item[0] == 'DE':
                items_manual_nueva += [item]
            elif tenant_actual.actores.dirigentes and item[0] == 'DI':
                items_manual_nueva += [item]
            elif tenant_actual.actores.escenarios and item[0] == 'ES':
                items_manual_nueva += [item]
            elif tenant_actual.actores.escuelas_deportivas and item[0] == 'EC':
                items_manual_nueva += [item]
            elif tenant_actual.actores.eventos and item[0] == 'EV':
                items_manual_nueva += [item]
            elif tenant_actual.actores.listados_doping and item[0] == 'LD':
                items_manual_nueva += [item]
            elif tenant_actual.actores.normas and item[0] == 'NO':
                items_manual_nueva += [item]
            elif tenant_actual.actores.noticias and item[0] == 'NT':
                items_manual_nueva += [item]
            elif tenant_actual.actores.personal_apoyo and item[0] == 'PA':
                items_manual_nueva += [item]
            elif tenant_actual.actores.publicidad and item[0] == 'PU':
                items_manual_nueva += [item]
            elif tenant_actual.actores.selecciones and item[0] == 'SE':
                items_manual_nueva += [item]
            elif tenant_actual.actores.respuesta and item[0] == 'SR':
                items_manual_nueva += [item]
            elif tenant_actual.actores.solicitud and item[0] == 'SS':
                items_manual_nueva += [item]

    articulos = encontrar_articulos_tenant(tenant_actual)
    entidades = filtrar_entidades(entidades, tenant_actual)

    return render(request, 'tree_list.html', {
        'articulos': articulos,
        'mensaje': mensaje,
        'items': items_manual_nueva,
        'entidades': entidades,
        'abrir_tree': abrir_tree

    })