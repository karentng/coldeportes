from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from snd.models import Deportista
from api_interoperable.models import DeportistaSerializable
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from entidades.models import Entidad
from django.db import connection
# Create your views here.

@api_view(['GET', 'POST'])
def deportista_get_post(request,format=None):
    ent = Entidad.objects.get(schema_name='club')

    if request.method == 'GET':
        connection.set_tenant(ent)
        deportistas = Deportista.objects.all()
        serializer = DeportistaSerializable(deportistas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        connection.set_tenant(ent)
        serializer = DeportistaSerializable(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT','DELETE'])
def deportista_detail_put_delete(request,pk,format=None):
    try:
        deportista = Deportista.objects.get(pk=pk)
    except Deportista.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DeportistaSerializable(deportista)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DeportistaSerializable(deportista, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        deportista.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


