from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from coldeportes.utilities import all_permission_required
from manual.models import Articulo
from manual.forms import ArticuloForm

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

    mensaje = "No hay artísulos registrados."

    return render(request, 'listar_articulo.html', {
        'articulos': articulos,
        'mensaje': mensaje,
        'items': items_manual,
        'articulo': articulo,

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
    articulos = Articulo.objects.all()

    mensaje = "No hay artísulos registrados."

    return render(request, 'tree_list.html', {
        'articulos': articulos,
        'mensaje': mensaje,
        'items': items_manual,

    })