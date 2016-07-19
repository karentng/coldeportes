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
from entidades.models import *
from django.http import HttpResponse
from django.db import connection

# Create your views here.

#Funciones generales para listado y recuperacion de deportistas en modelo adicionales a deportista
def get_model_by_tenant(request,method):
    """
    Funcion general. Permite seguir el comportamiento de listado o recuperacion jerarquico para Ligas, Federaciones y Publico.
    Busca retornar el listado o objeto de modelos adicionales a deportista segun la entidad solicitada por parametro
    Valida que la entidad a la que se quiere consultar petenezca a la jerarquia de la entidad quien solicita
    :param self: Objeto de modelo adicional a deportista
    :param request: Peticion
    :param viewset: Clase viewset del modelo adicional a deportista
    :return: Litado (o objeto) de modelos adicional a deportistas (o modelo deportista) de una entidad pasada por parametro o de un club que requiera consultarse a si mismo
    """
    if type(request.tenant.obtenerTenant()) in [Liga, LigaParalimpica, Federacion, FederacionParalimpica, Entidad]:
        if 'entidad' in request.query_params:
            entidad_name = request.query_params.get('entidad')
            try:
                entidad = Entidad.objects.get(schema_name=entidad_name)
                if not type(entidad.obtenerTenant()) in [Club,ClubParalimpico]:
                    raise Entidad.DoesNotExist
            except Entidad.DoesNotExist:
                return Response("No existe el Club o Club Paralimpico solicitado", status=status.HTTP_404_NOT_FOUND)
            if not validate_hierarchy(entidad.obtenerTenant(),request.tenant.obtenerTenant()):
                return Response("El club solicitado NO esta dentro de la jerarquia de la entidad quien solicita",status=status.HTTP_401_UNAUTHORIZED)
            connection.set_tenant(entidad)
            response = method(request)
            connection.set_tenant(request.tenant)
            return response
        else:
            return Response("Para hacer este tipo de consultas al nivel de jerarquia que se encuentra, es necesario que ingrese por parametro la entidad a consultar: entidad=schema_name",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return method(request)

def validate_hierarchy(club,tenant):
    """
    Funcion que permite validar la jerarquia de consultas, es decir, permita saber si se puede retornar la informacion del club que se solicita al tenant que lo solicita
    :param club: club al cual se va a consultar
    :param tenant: tenant quien solicita
    :return: permitido o no
    """
    if type(tenant) == Entidad:
        return True
    liga_federacion = club.liga if club.liga == None or type(tenant) in [Liga,LigaParalimpica] else club.liga.federacion
    return liga_federacion == tenant

#Fin funciones generales para listado de modelos adicionales a deportistas

class AddChangePermission(permissions.BasePermission):
    """
    Clase que define el permiso para editar , crear y eliminar deportistas
    """
    SAFE_METHODS=['POST','PUT','DELETE','PATCH']

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            if type(request.tenant.obtenerTenant()) == Club or type(request.tenant.obtenerTenant()) == ClubParalimpico:
                return request.user.has_perm("snd.add_deportista")
            else:
                return False
        return request.user.has_perm("snd.view_deportista")

class DeportistaViewSet(viewsets.ModelViewSet):
    """
    Vista encargada de get, post, put, delete , patch de modelo deportista
    """
    queryset = Deportista.objects.all()
    serializer_class = DeportistaSerializable
    permission_classes = (permissions.IsAuthenticated,AddChangePermission,)

    def list(self,request):
        """
            Permite retornar el listado de deportistas de acuerdo al tenant actual.
            En caso de ser Liga, Federacion o Publico se utilizan las vistas para obtencion de datos
            Para obtener un listado de una entidad particular dentro de la jerarquia debe pasarse como parametro el valor de entidad
            :param request: peticion
        """

        if type(request.tenant.obtenerTenant()) in [Entidad,LigaParalimpica,Liga,FederacionParalimpica,Federacion]:
            if 'entidad' in request.query_params:
                return get_model_by_tenant(request,super(DeportistaViewSet,self).list)
            else:
                clase = PublicDeportistaView if type(request.tenant.obtenerTenant()) == Entidad else TenantDeportistaView
                self.queryset = clase.objects.exclude(estado=3).distinct('id','entidad')
                self.serializer_class = DeportistasPublicSerializable if type(request.tenant.obtenerTenant()) == Entidad else DeportistaListSerializable
                return super(DeportistaViewSet,self).list(request)
        else:
            return super(DeportistaViewSet,self).list(request)

    def retrieve(self, request, *args, **kwargs):
        """
        Funcion que permite hacer la recuperacion de un objeto deportista de acuerdo a su id. Soporta busquedas jerarquicas pasando como parametro el valor entidad
        :param request: Peticion realizada
        :return: Objeto deportista del club solicitante o de una entidad pasada por parametro
        """
        return get_model_by_tenant(request,super(DeportistaViewSet,self).retrieve)

    def perform_create(self, serializer):
        """
        Permite validar si la entidad proveniente del deportista corresponde a la del request
        :param serializer: clase encargada de serializar el objeto
        """
        serializer.save(entidad=self.request.tenant, estado=0)

    def perform_destroy(self,instance):
        """
        Permite cambiar el estado del deportista en vez de eliminarlo de la base de datos (Borrado logico)
        :param instance: instancia a aplicar DELETE
        """
        if instance.estado == 0:
            instance.estado = 1
        else:
            instance.estado = 0
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


#API REST para modelo Composicion Corporal
class ComposicionCorporalViewSet(mixins.CreateModelMixin,
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

    def list(self, request, *args, **kwargs):
        """
        Funcion encargada de retornar el listado de composicion corporal de una entidad:
        *En caso de ser CLUB o CLUB PARALIMPICO - Retorna el listado de composicion corporal del club
        *En caso de ser LIGA , FEDERACION, PUBLIC - Se debe pasar por parametro el valor entidad, si esa entidad pertenece a la liga o federacion se retorna el listado de dicha entidad (debe ser un club)
        :param request: peticion
        :return: Listado de composiciones corporales
        """
        if 'deportista' in request.query_params:
            self.queryset = ComposicionCorporal.objects.filter(deportista = request.query_params.get('deportista'))
        return get_model_by_tenant(request,super(ComposicionCorporalViewSet,self).list)

    def retrieve(self, request, *args, **kwargs):
        """
            Funcion que permite hacer la recuperacion de un objeto composicion corporal de acuerdo a su id. Soporta busquedas jerarquicas pasando como parametro el valor entidad
            :param request: Peticion realizada
            :return: Objeto composicion corporal del club solicitante o de una entidad pasada por parametro
            """
        return get_model_by_tenant(request,super(ComposicionCorporalViewSet,self).retrieve)

#API REST para modelo historial deportivo
class HistorialDeportivoViewSet(mixins.CreateModelMixin,
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


    def list(self, request, *args, **kwargs):
        """
            Funcion encargada de retornar el listado de historial deportivo de una entidad:
            *En caso de ser CLUB o CLUB PARALIMPICO - Retorna el listado de historial deportivo del club
            *En caso de ser LIGA , FEDERACION, PUBLIC - Se debe pasar por parametro el valor entidad, si esa entidad pertenece a la liga o federacion se retorna el listado de dicha entidad (debe ser un club)
            :param request: peticion
            :return: Listado de historial deportivo
            """
        if 'deportista' in request.query_params:
            self.queryset = HistorialDeportivo.objects.filter(deportista=request.query_params.get('deportista'))
        return get_model_by_tenant(request, super(HistorialDeportivoViewSet,self).list)

    def retrieve(self, request, *args, **kwargs):
        """
            Funcion que permite hacer la recuperacion de un objeto historial deportivo de acuerdo a su id. Soporta busquedas jerarquicas pasando como parametro el valor entidad
            :param request: Peticion realizada
            :return: Objeto historial deportivo del club solicitante o de una entidad pasada por parametro
            """
        return get_model_by_tenant(request, super(HistorialDeportivoViewSet,self).retrieve)

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

    def list(self, request, *args, **kwargs):
        """
            Funcion encargada de retornar el listado de informacion academica de una entidad:
            *En caso de ser CLUB o CLUB PARALIMPICO - Retorna el listado de informacion academica del club
            *En caso de ser LIGA , FEDERACION, PUBLIC - Se debe pasar por parametro el valor entidad, si esa entidad pertenece a la liga o federacion se retorna el listado de dicha entidad (debe ser un club)
            :param request: peticion
            :return: Listado de informacion academica
            """
        if 'deportista' in request.query_params:
            self.queryset = InformacionAcademica.objects.filter(deportista=request.query_params.get('deportista'))
        return get_model_by_tenant(request, super(InformacionAcademicaViewSet,self).list)

    def retrieve(self, request, *args, **kwargs):
        """
            Funcion que permite hacer la recuperacion de un objeto informacion academica de acuerdo a su id. Soporta busquedas jerarquicas pasando como parametro el valor entidad
            :param request: Peticion realizada
            :return: Objeto informacion academica del club solicitante o de una entidad pasada por parametro
            """
        return get_model_by_tenant(request, super(InformacionAcademicaViewSet,self).retrieve)

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


    def list(self, request, *args, **kwargs):
        """
            Funcion encargada de retornar el listado de informacion adicional de una entidad:
            *En caso de ser CLUB o CLUB PARALIMPICO - Retorna el listado de informacion adicional del club
            *En caso de ser LIGA , FEDERACION, PUBLIC - Se debe pasar por parametro el valor entidad, si esa entidad pertenece a la liga o federacion se retorna el listado de dicha entidad (debe ser un club)
            :param request: peticion
            :return: Listado de informacion adicional
            """
        if 'deportista' in request.query_params:
            self.queryset = InformacionAdicional.objects.filter(deportista=request.query_params.get('deportista'))
        return get_model_by_tenant(request, super(InformacionAdicionalViewSet,self).list)

    def retrieve(self, request, *args, **kwargs):
        """
            Funcion que permite hacer la recuperacion de un objeto informacion adicional de acuerdo a su id. Soporta busquedas jerarquicas pasando como parametro el valor entidad
            :param request: Peticion realizada
            :return: Objeto informacion adicional del club solicitante o de una entidad pasada por parametro
            """
        return get_model_by_tenant(request, super(InformacionAdicionalViewSet, self).retrieve)

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

    def list(self, request, *args, **kwargs):
        """
            Funcion encargada de retornar el listado de historial de lesiones de una entidad:
            *En caso de ser CLUB o CLUB PARALIMPICO - Retorna el listado de historial de lesiones del club
            *En caso de ser LIGA , FEDERACION, PUBLIC - Se debe pasar por parametro el valor entidad, si esa entidad pertenece a la liga o federacion se retorna el listado de dicha entidad (debe ser un club)
            :param request: peticion
            :return: Listado de historial de lesiones
            """
        if 'deportista' in request.query_params:
            self.queryset = HistorialLesiones.objects.filter(deportista=request.query_params.get('deportista'))
        return get_model_by_tenant(request, super(HistorialLesionesViewSet,self).list)

    def retrieve(self, request, *args, **kwargs):
        """
            Funcion que permite hacer la recuperacion de un objeto historial lesiones de acuerdo a su id. Soporta busquedas jerarquicas pasando como parametro el valor entidad
            :param request: Peticion realizada
            :return: Objeto historial lesiones del club solicitante o de una entidad pasada por parametro
            """
        return get_model_by_tenant(request, super(HistorialLesionesViewSet, self).retrieve())