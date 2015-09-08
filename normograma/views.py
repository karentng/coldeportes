from django.shortcuts import render
from normograma.forms import NormaForm

# Create your views here.
def registrar(request):
    norma_form = NormaForm( )

    if request.method == 'POST':

        norma_form = NormaForm(request.POST)

        if norma_form.is_valid():
            norma_form.save()
            
            return redirect('listar_escenario')


    return render(request, 'normograma_registrar.html', {
        #'titulo': 'Identificación del Escenario',
        #'wizard_stage': 1,
        'form': norma_form,
    })
