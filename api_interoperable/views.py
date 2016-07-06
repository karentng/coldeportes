from django.shortcuts import render
from snd.models import Deportista,ComposicionCorporal,HistorialDeportivo,InformacionAcademica,InformacionAdicional,HistorialLesiones
from api_interoperable.models import DeportistaSerializable,ComposicionCorporalSerializable,HistorialDeportivoSerializable,InformacionAcademicaSerializable,HistorialLesionesSerializable,InformacionAdicionalSerializable
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
# Create your views here.
"""@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'deportistas': reverse('deportista-list',request=request,format=format)
        }
    )
"""
class AddChangePermission(permissions.BasePermission):
    """
    Clase que define el permiso para editar , crear y eliminar deportistas
    """
    SAFE_METHODS=['POST','PUT','DELETE','PATCH']

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            return request.user.has_perm("snd.add_deportista")
        return True

#API REST para modelo Deportista
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
        serializer.save(entidad=self.request.tenant)


class DeportistaDetail(generics.RetrieveUpdateAPIView):
    """
    Clase encargada del put, delete y get personal
    """
    queryset = Deportista.objects.all()
    serializer_class = DeportistaSerializable
    permission_classes = (permissions.IsAuthenticated,AddChangePermission,)

    def perform_destroy(self,instance):
        """
        Permite cambiar el estado del deportista en vez de eliminarlo de la base de datos (Borrado logico)
        :param instance: instancia a aplicar DELETE
        """
        instance.estado = 1
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

#API REST para modelo Composicion Corporal
class ComposcionCorporalList(generics.ListCreateAPIView):
    """
        Clase encargada de get y post de composicion corporal de deportista
        """
    queryset = ComposicionCorporal.objects.all()
    serializer_class = ComposicionCorporalSerializable
    permission_classes = (permissions.IsAuthenticated, AddChangePermission,)

class ComposcionCorporalDetail(generics.RetrieveUpdateAPIView):
    """
    Clase encargada del put, delete y get personal de composicion corporal de deportista
    """
    queryset = ComposicionCorporal.objects.all()
    serializer_class = ComposicionCorporalSerializable
    permission_classes = (permissions.IsAuthenticated,AddChangePermission,)

    def perform_destroy(self,instance):
        return Response(status=status.HTTP_204_NO_CONTENT)

#API REST para modelo historial deportivo
class HistorialDeportivolList(generics.ListCreateAPIView):
    """
        Clase encargada de get y post de composicion corporal de deportista
        """
    queryset = HistorialDeportivo.objects.all()
    serializer_class = HistorialDeportivoSerializable
    permission_classes = (permissions.IsAuthenticated, AddChangePermission,)

class HistorialDeportivoDetail(generics.RetrieveUpdateAPIView):
    """
    Clase encargada del put, delete y get personal de composicion corporal de deportista
    """
    queryset = HistorialDeportivo.objects.all()
    serializer_class = HistorialDeportivoSerializable
    permission_classes = (permissions.IsAuthenticated,AddChangePermission,)

    def perform_destroy(self, instance):
        return Response(status=status.HTTP_204_NO_CONTENT)