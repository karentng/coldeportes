from django.shortcuts import render
from snd.models import Deportista,ComposicionCorporal,HistorialDeportivo,InformacionAcademica,InformacionAdicional,HistorialLesiones
from api_interoperable.models import DeportistaSerializable,ComposicionCorporalSerializable,HistorialDeportivoSerializable,InformacionAcademicaSerializable,HistorialLesionesSerializable,InformacionAdicionalSerializable, DeportistasPublicSerializable, DeportistaListSerializable
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets,mixins
from entidades.modelos_vistas_reportes import PublicDeportistaView
from reportes.models import TenantDeportistaView
import urllib.request, base64
from entidades.models import *
from rest_framework.pagination import PageNumberPagination

# Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
    """
    Vista encargada de mostrar la estructura de la API REST
    """
    return Response(
        {
            'basico': reverse('deportista-list',request=request,format=format),
            'corporal': reverse('corporal-list',request=request,format=format),
            'deportivo': reverse('deportivo-list',request=request,format=format),
            'academico': reverse('academico-list',request=request,format=format),
            'adicional': reverse('adicional-list',request=request,format=format),
            'lesiones': reverse('lesiones-list',request=request,format=format),

        }
    )

class AddChangePermission(permissions.BasePermission):
    """
    Clase que define el permiso para editar , crear y eliminar deportistas
    """
    SAFE_METHODS=['POST','PUT','DELETE','PATCH']

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            return request.user.has_perm("snd.add_deportista")
        return True

class DeportistaViewSet(viewsets.ModelViewSet):
    """
    Vista encargada de get, post, put, delete , patch de modelo deportista
    """
    queryset = Deportista.objects.all()
    serializer_class = DeportistaSerializable
    permission_classes = (permissions.IsAuthenticated,AddChangePermission,)

    def list(self,request):
        """
            Permite retornar el listado de deportistas de acuerdo al tenant actual
            :param request: peticion
        """
        if type(request.tenant.obtenerTenant()) is Entidad:
            queryset = PublicDeportistaView.objects.exclude(estado=3).distinct('id','entidad')
            serializer = DeportistasPublicSerializable
        elif type(request.tenant.obtenerTenant()) is Federacion or type(request.tenant.obtenerTenant()) is Liga:
            queryset = TenantDeportistaView.objects.exclude(estado=3).distinct('id','entidad')
            serializer = DeportistaListSerializable
        else:
            queryset = Deportista.objects.all()
            serializer = DeportistaSerializable

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Permite validar si la entidad proveniente del deportista corresponde a la del request
        :param serializer: clase encargada de serializar el objeto
        """
        serializer.save(entidad=self.request.tenant)

    def perform_destroy(self,instance):
        """
        Permite cambiar el estado del deportista en vez de eliminarlo de la base de datos (Borrado logico)
        :param instance: instancia a aplicar DELETE
        """
        instance.estado = 1
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


#API REST para modelo Composicion Corporal
class ComposcionCorporalViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    Vista encargada de get, post, put , patch de modelo composicion corporal
    """
    queryset = ComposicionCorporal.objects.all()
    serializer_class = ComposicionCorporalSerializable
    permission_classes = (permissions.IsAuthenticated, AddChangePermission,)

#API REST para modelo historial deportivo
class HistorialDeportivolViewSet(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):
    """
    Vista encargada de get, post, put , patch de historial deportivo de deportista
    """
    queryset = HistorialDeportivo.objects.all()
    serializer_class = HistorialDeportivoSerializable
    permission_classes = (permissions.IsAuthenticated, AddChangePermission,)

#API REST para modelo informacion academica
class InformacionAcademicaViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.RetrieveModelMixin,
                               viewsets.GenericViewSet):
    """
    Vista encargada de get, post, put , patch de informacion academica de deportista
    """
    queryset = InformacionAcademica.objects.all()
    serializer_class = InformacionAcademicaSerializable
    permission_classes = (permissions.IsAuthenticated, AddChangePermission,)

#API REST para modelo informacion adicional
class InformacionAdicionalViewSet(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):
    """
    Clase encargada de get, post, put, patch de informacion adicional de deportista
    """
    queryset = InformacionAdicional.objects.all()
    serializer_class = InformacionAdicionalSerializable
    permission_classes = (permissions.IsAuthenticated, AddChangePermission,)

#API REST para modelo historial lesiones
class HistorialLesionesViewSet(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):
    """
    Clase encargada de get , post, put , patch de historial lesioaes de deportista
    """
    queryset = HistorialLesiones.objects.all()
    serializer_class = HistorialLesionesSerializable
    permission_classes = (permissions.IsAuthenticated, AddChangePermission,)