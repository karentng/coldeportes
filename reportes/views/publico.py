#encoding:utf-8
from django.shortcuts import render, redirect

def tipos(request):
    return render(request, 'publico/tipos.html', {
    })