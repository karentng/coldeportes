#encoding:utf-8
from django.shortcuts import render, redirect

def demografia(request):
    return render(request, 'caf/demografia.html', {
    })