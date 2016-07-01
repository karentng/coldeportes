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
# Create your views here.

class DeportistasList(APIView):
    """
    Clase encargada de get y post de deportistas
    """

    def get(self,request,format=None):
        deportistas = Deportista.objects.all()
        serializer = DeportistaSerializable(deportistas, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = DeportistaSerializable(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DeportistaDetail(APIView):
    """
    Clase encargada del put, delete y get personal
    """

    def get_object(self,pk):
        try:
            return Deportista.objects.get(id=pk)
        except Deportista.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        deportista = self.get_object(pk)
        serializer = DeportistaSerializable(deportista)
        return Response(serializer.data)

    def put(self,request, pk, format=None):
        deportista = self.get_object(pk)
        serializer = DeportistaSerializable(deportista,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk, format=None):
        deportista = self.get_object(pk)
        deportista.estado = 1
        deportista.save()
        return Response(status=status.HTTP_204_NO_CONTENT)