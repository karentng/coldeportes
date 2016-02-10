from django.shortcuts import render
from snd.models import Deportista
from api_interoperable.models import DeportistaSerializable
from django.http import JsonResponse
# Create your views here.
def get_deportista(request):
    depor = Deportista.objects.all()[0]
    seri = DeportistaSerializable(depor)
    return JsonResponse(seri.data)

