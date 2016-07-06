from django.shortcuts import render
from entidades.models import Federacion,Liga,Entidad,Club,ClubParalimpico
from snd.models import Deportista,ComposicionCorporal,HistorialDeportivo,InformacionAcademica,InformacionAdicional,HistorialLesiones
from api_interoperable.models import DeportistaSerializable,ComposicionCorporalSerializable,HistorialDeportivoSerializable,InformacionAcademicaSerializable,HistorialLesionesSerializable,InformacionAdicionalSerializable
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets,mixins
from django.db import connection
from django.shortcuts import get_object_or_404
from entidades.modelos_vistas_reportes import PublicDeportistaView
from reportes.models import TenantDeportistaView

# Create your views here.
def get_deportista(entidades):
    pass

def organizar_deportistas(tenant):
    """
    Hacer peticiones get a cada uno de los tenants y juntar los json en un arreglo
    :param tenant:
    :return:
    """
    if tenant.obtenerTenant.__class__ == Entidad:
        clubs = [club.nombre for club in Club.objects.all()]
        clubs_paralimpicos = [club.nombre for club in ClubParalimpico.objects.all()]

    elif tenant.obtenerTenant.__class__ == Federacion:
        ligas = tenant.ligas_asociadas()
    elif tenant.obtenerTenant.__class__ == Liga:
        pass
    else:
        pass


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
    """
    def list(self,request):
        if request.tenant == 'public':
            queryset = TenantDeportistaView.objects.distinct('id')
        else:
            queryset = PublicDeportistaView.objects.distinct('id')

        serializer = DeportistaSerializable(queryset,many=True)
        return Response(serializer.data)
    """
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
    queryset = HistorialDeportivo.objects.all()
    serializer_class = HistorialDeportivoSerializable
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