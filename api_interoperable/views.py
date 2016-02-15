from django.shortcuts import render
from snd.models import Deportista
from api_interoperable.models import DeportistaSerializable
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from entidades.models import Entidad
from django.db import connection
from django.http import JsonResponse
# Create your views here.

@api_view(['GET', 'POST'])
def deportista_list(request,format=None):
    ent = Entidad.objects.get(schema_name='deporcali')

    if request.method == 'GET':
        connection.set_tenant(ent)
        deportistas = Deportista.objects.all()
        serializer = DeportistaSerializable(deportistas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        connection.set_tenant(ent)
        serializer = DeportistaSerializable(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

