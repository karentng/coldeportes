from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from snd.models import Deportista
from api_interoperable.models import DeportistaSerializable
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics
# Create your views here.

class DeportistasList(generics.ListCreateAPIView):
    """
    Clase encargada de get y post de deportistas
    """
    queryset = Deportista.objects.all()
    serializer_class = DeportistaSerializable

class DeportistaDetail(generics.RetrieveUpdateAPIView):
    """
    Clase encargada del put, delete y get personal
    """
    queryset = Deportista.objects.all()
    serializer_class = DeportistaSerializable

    def delete(self,request,pk, format=None):
        try:
            deportista = self.queryset.get(id=pk)
        except Deportista.DoesNotExist:
            raise Http404
        deportista.estado = 1
        deportista.save()
        return Response(status=status.HTTP_204_NO_CONTENT)