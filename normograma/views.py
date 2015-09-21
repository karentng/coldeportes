from django.shortcuts import render, redirect
from normograma.forms import NormaForm, NormogramaBusquedaForm
from django.contrib.auth.decorators import login_required
from normograma.models import Norma


@login_required
def registrar(request):
    """
    Septiembre 14 / 2015
    Autor: Karent Narvaez Grisales
    
    registro de la información de una norma en el módulo de normograma.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    norma_form = NormaForm( )

    if request.method == 'POST':

        norma_form = NormaForm(request.POST)

        if norma_form.is_valid():
            norma_form.save()
            
            return redirect('listar_escenarios')


    return render(request, 'normograma_registrar.html', {
        'form': norma_form,
    })

@login_required
def buscar(request):
    """
    Septiembre 14 / 2015
    Autor: Karent Narvaez Grisales
    
    realizar búsqueda de los diferentes criterios para una norma registrada en el normograma.

    Se obtienen los resultados que coinciden con la búsqueda..

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
      

    #inicializado formulario de búsqueda
    form = NormogramaBusquedaForm()

    #inicialización de variable resultados
    listado_resultados = []
    cantidad_resultados = 0

    if request.method == 'POST':
        
        form = NormogramaBusquedaForm(request.POST)


        if form.is_valid():
            sectores = request.POST.getlist('sector') or None
            jurisdicciones = request.POST.getlist('jurisdiccion') or None
            texto = request.POST.get('texto_a_buscar') or ''

            normas = Norma.objects.filter(contenido_busqueda__icontains=texto)

                              
        listado_resultados.append(normas)
        cantidad_resultados = len(listado_resultados[0])

    return render(request, 'normograma_buscar.html', {
        'form': form,
        'listado_resultados': listado_resultados,
        'cantidad_resultados': cantidad_resultados,
    })