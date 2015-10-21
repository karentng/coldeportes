from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import NoticiaForm
from .models import Noticia

# Create your views here.
def registrar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Se ha registrado la noticia correctamente')
            return redirect('listar_noticias')
    else:
        form = NoticiaForm()
    return render(request,'registrar_noticia.html',{'form':form})


def listar_noticias(request):
    noticias = Noticia.objects.all()

    return render(request,'listar_noticias.html',{'noticias':noticias})


def editar_noticia(request,id_noticia):
    try:
        noticia = Noticia.objects.get(id=id_noticia)
    except Exception:
        messages.error(request,'La noticia que está intentando editar no existe')
        return redirect('listar_noticias')

    form = NoticiaForm(instance=noticia)

    if request.method=='POST':
        form = NoticiaForm(request.POST,request.FILES,instance=noticia)
        if form.has_changed:
            if form.is_valid():
                form.save()
                messages.success(request,'La noticia se ha editado correctamente')
                return redirect('listar_noticias')
    return render(request,'registrar_noticia.html',{'form':form,
                                               'edicion':True})


def eliminar_noticia(request,id_noticia):
    try:
        Noticia.objects.get(id=id_noticia).delete()
    except Exception:
        messages.error(request,'La noticia que está intentando eliminar no existe')
        return redirect('listar_noticias')
    messages.success(request,'Se ha eliminado la noticia correctamente')
    return redirect('listar_noticias')

