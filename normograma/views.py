from django.shortcuts import render, redirect
from normograma.forms import NormaForm, NormogramaBusquedaForm
from django.contrib.auth.decorators import login_required
from normograma.models import Norma
from django.contrib import messages


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

        norma_form = NormaForm(request.POST, request.FILES)

        if norma_form.is_valid():
            norma_form.save()
            
            return redirect('normograma_buscar')


    return render(request, 'normograma_registrar.html', {
        'form': norma_form,
    })

@login_required
def editar(request, norma_id):
    """
    Septiembre 14 / 2015
    Autor: Karent Narvaez Grisales
    
    editar de la información de una norma en el módulo de normograma.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param norma_id:  norma_id
    :type norma_id:   
    """

    try:
        norma = Norma.objects.get(id = norma_id)
    except Exception:
        norma = None

    norma_form = NormaForm(instance = norma)

    if request.method == 'POST':

        norma_form = NormaForm(request.POST, request.FILES, instance = norma)

        if norma_form.is_valid():
            norma_form.save()
            messages.success(request, "Norma modificada correctamente.")
            return redirect('normograma_buscar')


    return render(request, 'normograma_registrar.html', {
        'form': norma_form,
    })

def buscarPorSectores(sectores, texto):
    normas = []

    for sector in sectores:
        normas += list(Norma.objects.filter(contenido_busqueda__icontains=texto, sectores=sector).distinct('id'))

    return normas  
      
def buscarPorJurisdicciones(jurisdicciones, texto):
    normas = []

    for jurisdiccion in jurisdicciones:
        normas += list(Norma.objects.filter(contenido_busqueda__icontains=texto, jurisdiccion=jurisdiccion).distinct('id'))

    return normas

def buscarPorSectoresYJurisdicciones(sectores,jurisdicciones, texto):
    normas = []

    for jurisdiccion in jurisdicciones:
        for sector in sectores:
            normas += list(Norma.objects.filter(contenido_busqueda__icontains=texto, sectores=sector, jurisdiccion=jurisdiccion).distinct('id'))

    return normas

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
    primer_resultado = None

    if request.method == 'POST':
        
        form = NormogramaBusquedaForm(request.POST)


        if form.is_valid():
            sectores = request.POST.getlist('sector') or None
            jurisdicciones = request.POST.getlist('jurisdiccion') or None
            texto = request.POST.get('texto_a_buscar') or ''

            if sectores and not jurisdicciones:
                normas = buscarPorSectores(sectores, texto)
            elif jurisdicciones and not sectores:
                normas = buscarPorJurisdicciones(jurisdicciones, texto)
            elif sectores and jurisdicciones:
                normas = buscarPorSectoresYJurisdicciones(sectores, jurisdicciones, texto)
            else:
                normas = Norma.objects.filter(contenido_busqueda__icontains=texto)
                              
        listado_resultados.append(normas)
        cantidad_resultados = len(listado_resultados[0])
        primer_resultado = listado_resultados[0]

    return render(request, 'normograma_buscar.html', {
        'form': form,
        'listado_resultados': listado_resultados,
        'cantidad_resultados': cantidad_resultados,
        'primer_resultado': primer_resultado
    })