from django.shortcuts import render
from snd.models import Deportista
from api_interoperable.models import DeportistaSerializable
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework import generics
from rest_framework import permissions
# Create your views here.
class AddChangePermission(permissions.BasePermission):
    """
    Clase que define el permiso para editar , crear y eliminar deportistas
    """
    SAFE_METHODS=['POST','PUT','DELETE','PATCH']

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            return request.user.has_perm("snd.add_deportista")
        return True


class DeportistasList(generics.ListCreateAPIView):
    """
    Clase encargada de get y post de deportistas
    """
    queryset = Deportista.objects.all()
    serializer_class = DeportistaSerializable
    permission_classes = (permissions.IsAuthenticated,AddChangePermission,)

    def perform_create(self, serializer):
        """
        Permite validar si la entidad proveniente del deportista corresponde a la del request
        :param serializer: clase encargada de serializar el objeto
        """
        entidad_registrada = serializer.data["entidad"]
        entidad_request = self.request.tenant.id
        if entidad_registrada != entidad_request:
            raise serializer.ValidationError("Entidad no corresponde")
        serializer.save()

class DeportistaDetail(generics.RetrieveUpdateAPIView):
    """
    Clase encargada del put, delete y get personal
    """
    queryset = Deportista.objects.all()
    serializer_class = DeportistaSerializable
    permission_classes = (permissions.IsAuthenticated,AddChangePermission,)

    def delete(self,request,pk, format=None):
        try:
            deportista = self.queryset.get(id=pk)
        except Deportista.DoesNotExist:
            raise Http404
        deportista.estado = 1
        deportista.save()
        return Response(status=status.HTTP_204_NO_CONTENT)