from django.db import models
from tenant_schemas.models import TenantMixin
from coldeportes.utilities import permisos_de_tipo

class Departamento(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='nombre')
    codigo = models.CharField(max_length=10, null=True, verbose_name='código')
    latitud = models.FloatField(null=True)
    longitud = models.FloatField(null=True)

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='nombre')
    departamento = models.ForeignKey(Departamento)
    codigo = models.CharField(max_length=10, null=True, verbose_name='código')
    latitud = models.FloatField(null=True)
    longitud = models.FloatField(null=True)

    def __str__(self):
        return ("%s (%s)")%(self.nombre, self.departamento.nombre)

#General para deportistas y escenarios
class TipoDisciplinaDeportiva(models.Model):
    descripcion = models.CharField(max_length=50, verbose_name='descripción')

    def __str__(self):
        return self.descripcion

class ModalidadDisciplinaDeportiva(models.Model):
    tipo = models.ForeignKey(TipoDisciplinaDeportiva)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=50, verbose_name='descripción', blank=True)

    def __str__(self):
        return self.nombre

class CategoriaDisciplinaDeportiva(models.Model):
    modalidad = models.ForeignKey(ModalidadDisciplinaDeportiva)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=50, verbose_name='descripción', blank=True)

    def __str__(self):
        return self.nombre



class Actores(models.Model):
    centros = models.BooleanField(verbose_name="Centros de Acondicionamiento Físico")
    escenarios = models.BooleanField(verbose_name="Escenarios")
    deportistas = models.BooleanField(verbose_name="Deportistas")
    personal_apoyo = models.BooleanField(verbose_name="Personal de apoyo")
    dirigentes = models.BooleanField(verbose_name="Dirigentes")
    cajas = models.BooleanField(verbose_name="Cajas de Compensación")
    selecciones = models.BooleanField(verbose_name="Selecciones")
    centros_biomedicos = models.BooleanField(verbose_name="Centros Biomédicos")
    normas = models.BooleanField(verbose_name="Normograma")
    escuelas_deportivas = models.BooleanField(verbose_name="Escuelas de Formación Deportiva")

    def resumen(self):
        actores = []
        campos = self._meta.fields
        for i in campos:
            if getattr(self, i.name) == True and i.name != 'id':
                actores.append(i.verbose_name)
        return actores

class Entidad(TenantMixin): # Entidad deportiva
    TIPOS = (
        (1, 'Liga'),
        (2, 'Federación'),
        (3, 'Club'),
        (4, 'Cajas de Compensación'),
        (5, 'Ente'),
        (6, 'Comité'),
        (7,'Federación Paralimpica'),
        (8,'Liga Paralimpica'),
        (9,'Club Paralimpico'),
        (10,'Centro De Acondicionamiento'),
        (11, 'Escuela de Formación Deportiva'),
    )
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255, verbose_name="dirección")
    pagina_web = models.URLField(verbose_name="página web propia", blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad)
    telefono = models.CharField(max_length=255, verbose_name="teléfono", blank=True)
    descripcion = models.TextField(verbose_name="descripción", blank=True, null=True)

    tipo = models.IntegerField(choices=TIPOS)
    actores = models.OneToOneField(Actores, null=True)
    auto_create_schema = True

    #def ajustar_resultado(self, resultado, resultado_consulta):
    def ajustar_resultado(self, resultado):
        datos = {}
        for i in resultado:
            descripcion = i['descripcion']
            if descripcion in datos:
                datos[descripcion] += i['cantidad']
            else:
                datos[descripcion] = i['cantidad']
        return datos

    def ejecutar_consulta(self, ajustar, consulta):
        from django.db.models import Count, F
        from snd.modelos.cafs import CentroAcondicionamiento
        from snd.modelos.deportistas import HistorialDeportivo,InformacionAdicional,Deportista
        from datetime import date

        resultado = eval(consulta)
        if ajustar:
            resultado = self.ajustar_resultado(resultado)

        return resultado

    def obtenerTenant(self):
        if self.tipo == 1:
            modelo = Liga
        elif self.tipo == 2:
            modelo = Federacion
        elif self.tipo == 3:
            modelo = Club
        elif self.tipo == 4:
            modelo = CajaDeCompensacion
        elif self.tipo == 5:
            modelo = Ente
        elif self.tipo == 6:
            modelo = Comite
        elif self.tipo == 7:
            modelo= FederacionParalimpica
        elif self.tipo == 8:
            modelo = LigaParalimpica
        elif self.tipo == 9:
            modelo = ClubParalimpico
        elif self.tipo == 10:
            modelo = Caf
        elif self.tipo == 11:
            modelo = EscuelaDeportiva_

        try:
            return modelo.objects.get(id=self.id)
        except Exception:
            return self

    def deportistas_registrables(self):
        return permisos_de_tipo(self,[3,9])

    def disponible_para_transferencias(self):
        return permisos_de_tipo(self,[3,9])

    def seleccionable(self):
        return permisos_de_tipo(self,[1,2,6,7,8])

    def avalable(self):
        return permisos_de_tipo(self,[1,2,7,8])

    def atributos_escenarios(self):
        from snd.modelos.escenarios import Escenario
        todosEscenarios = Escenario.objects.filter(entidad=self)
        escenarios = []
        for i in todosEscenarios:
            escenarios.append(i.obtenerAtributos())
        
        return escenarios

    def atributos_cafs(self):
        from snd.modelos.cafs import CentroAcondicionamiento
        todosCentros = CentroAcondicionamiento.objects.filter(entidad=self)
        centros = []
        for i in todosCentros:
            centros.append(i.obtenerAtributos())
        
        return centros

    def atributos_deportistas(self):
        from snd.modelos.deportistas import Deportista
        todos_deportistas = Deportista.objects.filter(entidad=self)
        deportistas = []
        for i in todos_deportistas:
            deportistas.append(i.obtenerAtributos())

        return deportistas

    def atributos_personales_apoyo(self):
        from snd.modelos.personal_apoyo import PersonalApoyo
        todos_personales_apoyo = PersonalApoyo.objects.filter(entidad=self)
        personales_apoyo = []
        for i in todos_personales_apoyo:
            personales_apoyo.append(i.obtenerAtributos())

        return personales_apoyo

    def atributos_dirigentes(self):
        from snd.modelos.dirigentes import Dirigente
        todos_dirigentes = Dirigente.objects.filter(entidad=self)
        dirigentes = []
        for dirigente in todos_dirigentes:
            dirigentes.append(dirigente.obtenerAtributos())

        return dirigentes

    def atributos_cajas(self):
        from snd.modelos.cajas_compensacion import CajaCompensacion
        todas_cajas = CajaCompensacion.objects.filter(entidad=self)
        cajas = []
        for caja in todas_cajas:
            cajas.append(caja.obtenerAtributos())

        return cajas

    def atributos_centros_biomedicos(self):
        from snd.modelos.centro_biomedico import CentroBiomedico
        todos_centros = CentroBiomedico.objects.filter(entidad=self)
        centros = []
        for centro in todos_centros:
            centros.append(centro.obtenerAtributos())

        return centros

    def atributosDeSusActores(self):
        from django.db import connection
        def agregarActor(datos, booleano, identificador, metodo):
            if booleano:
                datos[identificador] = metodo()
            connection.set_tenant(self)
            return datos

        tenant = self.obtenerTenant()
        actores = tenant.actores

        datos = {}
        datos = agregarActor(datos, actores.centros, "caf", tenant.atributos_cafs)
        datos = agregarActor(datos, actores.escenarios, "escenarios", tenant.atributos_escenarios)
        datos = agregarActor(datos, actores.deportistas, "deportistas", tenant.atributos_deportistas)
        datos = agregarActor(datos, actores.personal_apoyo, "personales", tenant.atributos_personales_apoyo)
        datos = agregarActor(datos, actores.dirigentes, "dirigentes", tenant.atributos_dirigentes)
        datos = agregarActor(datos, actores.cajas, "cajas", tenant.atributos_cajas)
        datos = agregarActor(datos, actores.centros_biomedicos, "centros_biomedicos", tenant.atributos_centros_biomedicos)

        try:
            datos['ligas'] = tenant.ligas_asociadas()
        except Exception:
            pass

        try:
            datos['clubes'] = tenant.clubes_asociados()
        except Exception:
            pass

        return datos

    def cantidadActoresAsociados(self):
        atributosActores = self.atributosDeSusActores()

        def definirElementosDashBoard(datos, identificador, nombre, color, url,icono):
            try:
                cantidad = len(atributosActores[identificador])
                datos += [[nombre, color, cantidad, url,icono]]
            except KeyError:
                pass
            return datos
        
        datos = []
        
        definirElementosDashBoard(datos, "ligas", "Ligas", "black", "inicio_tenant","fa-building-o")
        definirElementosDashBoard(datos, "clubes", "Clubes", "black", "inicio_tenant","fa-building-o")
        definirElementosDashBoard(datos, "caf", "CAFs", "red", "listar_cafs","ion-android-bicycle")
        definirElementosDashBoard(datos, "escenarios", "Escenarios", "blue", "listar_escenarios","fa-bank")
        definirElementosDashBoard(datos, "deportistas", "Deportistas", "orange", "deportista_listar","ion-ribbon-a")
        definirElementosDashBoard(datos, "personales", "Personal de Apoyo", "green", "personal_apoyo_listar","ion-ios-body")
        definirElementosDashBoard(datos, "dirigentes", "Dirigentes", "purple", "dirigentes_listar","ion-ios-people")
        definirElementosDashBoard(datos, "cajas", "Cajas de Compensación", "black", "listar_ccfs","fa-building-o")
        definirElementosDashBoard(datos, "centros_biomedicos", "Centros Biomédicos ", "blue", "centro_biomedico_listar","ion-ios-body")

        return datos

    def posicionInicialMapa(self):
        tenant = self.obtenerTenant()
        try:
            ciudad = tenant.ciudad
        except Exception:
            ciudad = Ciudad.objects.get(nombre="Bogotá D.C.")
        
        coordenadas = [ciudad.latitud, ciudad.longitud]

        return coordenadas

    def __str__(self):
        return self.nombre

class Ente(Entidad):
    TIPOS_ENTE = (
        (1, 'Ente Municipal'),
        (2, 'Ente Departamental'),
    )
    tipo_ente = models.IntegerField(choices=TIPOS_ENTE)

    def obtener_datos_entidad(self):
        entidad = {
            'tipo_tenant': type(self).__name__,
            'mostrar_info':True,
            'nombre':self.nombre,
            'disciplina': None,
            'descripcion': self.descripcion,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'pagina_web': self.pagina_web,
            'disponible_para_transferencias' : self.disponible_para_transferencias()
        }
        return entidad

class Comite(Entidad):
    TIPOS_COMITE = (
        (1, 'Comité Olimpico Colombiano'),
        (2, 'Comité Paralímpico Colombiano'),
    )
    tipo_comite = models.IntegerField(choices=TIPOS_COMITE)

    def obtener_datos_entidad(self):
        entidad = {
            'tipo_tenant': type(self).__name__,
            'mostrar_info':True,
            'nombre':self.nombre,
            'disciplina': None,
            'descripcion': self.descripcion,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'pagina_web': self.pagina_web,
            'disponible_para_transferencias' : self.disponible_para_transferencias()
        }
        return entidad

class CajaDeCompensacion(Entidad):
    pass
    def obtener_datos_entidad(self):
        entidad = {
            'tipo_tenant': type(self).__name__,
            'mostrar_info':True,
            'nombre':self.nombre,
            'disciplina': None,
            'descripcion': self.descripcion,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'pagina_web': self.pagina_web,
            'disponible_para_transferencias' : self.disponible_para_transferencias()
        }
        return entidad

def ruta_resoluciones_reconocimiento(instance, filename):
    return "tenants/resoluciones/%s"%(filename.encode('ascii','ignore').decode('ascii'))

class ResolucionReconocimiento(Entidad):
    resolucion = models.CharField(max_length=255, blank=True, verbose_name="resolución de reconocimiento deportivo")
    fecha_resolucion = models.DateField(blank=True, null=True, verbose_name="fecha de resolución de reconocimiento deportivo")
    fecha_vencimiento = models.DateField(blank=True, null=True, verbose_name="fecha vencimiento de resolución de reconocimiento deportivo")
    archivo = models.FileField(upload_to=ruta_resoluciones_reconocimiento, blank=True, null=True, verbose_name="archivo de resolución de reconocimiento deportivo")

    class Meta:
        abstract = True

class FederacionParalimpica(ResolucionReconocimiento):
    DISCAPACIDADES = (
        (1,'Limitaciones Fisica'),
        (2,'Limitación Auditiva'),
        (3,'Limitación Visual'),
        (4,'Parálisis Cerebral'),
        (5,'Limitación Intelectual'),
    )
    discapacidad = models.IntegerField(choices=DISCAPACIDADES)
    comite = models.ForeignKey(Comite)

    def save(self, *args, **kwargs):
        comite_para = Comite.objects.get(tipo_comite=2)
        self.comite=comite_para
        super(FederacionParalimpica, self).save(*args, **kwargs)
    def obtener_datos_entidad(self):
        entidad = {
            'tipo_tenant': type(self).__name__,
            'mostrar_info':True,
            'nombre':self.nombre,
            'disciplina': self.discapacidad,
            'descripcion': self.descripcion,
            'ciudad': 'Colombia(Nacional)',
            'direccion': self.direccion,
            'telefono': self.telefono,
            'pagina_web': self.pagina_web,
            'disponible_para_transferencias' : self.disponible_para_transferencias()
        }
        return entidad

class LigaParalimpica(ResolucionReconocimiento):
    DISCAPACIDADES = (
        (1,'Limitaciones Fisicas'),
        (2,'Limitación Auditiva'),
        (3,'Limitación Visual'),
        (4,'Parálisis Cerebral'),
        (5,'Limitación Intelectual'),
    )
    discapacidad = models.IntegerField(choices=DISCAPACIDADES)
    federacion = models.ForeignKey(FederacionParalimpica)

    def obtener_datos_entidad(self):
        entidad = {
            'tipo_tenant': type(self).__name__,
            'mostrar_info':True,
            'nombre':self.nombre,
            'disciplina': self.discapacidad,
            'descripcion': self.descripcion,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'pagina_web': self.pagina_web,
            'disponible_para_transferencias' : self.disponible_para_transferencias()
        }
        return entidad


class ClubParalimpico(ResolucionReconocimiento):
    liga = models.ForeignKey(LigaParalimpica, null=True, blank=True)

    def historiales_para_avalar(self,tipo):
        from snd.models import HistorialDeportivo
        return [x.obtener_info_aval() for x in HistorialDeportivo.objects.filter(estado='Pendiente',tipo=tipo,deportista__estado=0)]

    def obtener_datos_entidad(self):
        entidad = {
            'tipo_tenant': type(self).__name__,
            'mostrar_info':True,
            'nombre':self.nombre,
            'disciplina': self.liga.discapacidad,
            'descripcion': self.descripcion,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'pagina_web': self.pagina_web,
            'disponible_para_transferencias' : self.disponible_para_transferencias()
        }
        return entidad

class Federacion(ResolucionReconocimiento):
    disciplina = models.ForeignKey(TipoDisciplinaDeportiva)
    comite = models.ForeignKey(Comite)

    def obtener_datos_entidad(self):
        entidad = {
            'tipo_tenant': type(self).__name__,
            'mostrar_info':True,
            'nombre':self.nombre,
            'disciplina': self.disciplina,
            'descripcion': self.descripcion,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'pagina_web': self.pagina_web,
            'disponible_para_transferencias' : self.disponible_para_transferencias()
        }
        return entidad

    def save(self, *args, **kwargs):
        comite = Comite.objects.get(tipo_comite=1)
        self.comite=comite
        super(Federacion, self).save(*args, **kwargs)

    def ligas_asociadas(self):
        ligas = Liga.objects.filter(federacion=self)
        return ligas

    def atributos_escenarios(self):
        from snd.modelos.escenarios import Escenario
        from django.db import connection
        escenarios = []

        todosEscenarios = Escenario.objects.filter(entidad=self)
        
        for i in todosEscenarios:
            escenarios.append(i.obtenerAtributos())

        ligas = Liga.objects.filter(federacion=self)
        for i in ligas:
            connection.set_tenant(i)
            escenarios += i.atributos_escenarios()

        return escenarios

    def atributos_cafs(self):
        from snd.modelos.cafs import CentroAcondicionamiento
        from django.db import connection

        centros = []

        todos_cafs = CentroAcondicionamiento.objects.filter(entidad=self)
        
        for i in todos_cafs:
            centros.append(i.obtenerAtributos())

        ligas = Liga.objects.filter(federacion=self)
        for i in ligas:
            connection.set_tenant(i)
            centros += i.atributos_cafs()
        
        return centros

    def atributos_deportistas(self):
        from snd.modelos.deportistas import Deportista
        from django.db import connection

        deportistas = []

        todos_deportistas = Deportista.objects.filter(entidad=self)

        for i in todos_deportistas:
            deportistas.append(i.obtenerAtributos())

        ligas = Liga.objects.filter(federacion=self)
        for i in ligas:
            connection.set_tenant(i)
            deportistas += i.atributos_deportistas()

        return deportistas

    def atributos_personales_apoyo(self):
        from snd.modelos.personal_apoyo import PersonalApoyo
        from django.db import connection

        personales_apoyo = []

        todos_personales_apoyo = PersonalApoyo.objects.filter(entidad=self)

        for i in todos_personales_apoyo:
            personales_apoyo.append(i.obtenerAtributos())

        ligas = Liga.objects.filter(federacion=self)
        for i in ligas:
            connection.set_tenant(i)
            personales_apoyo += i.atributos_personales_apoyo()

        return personales_apoyo

    def atributos_dirigentes(self):
        from snd.modelos.dirigentes import Dirigente
        from django.db import connection

        dirigentes = []

        todosDirigentes = Dirigente.objects.filter(entidad=self)

        for dirigente in todosDirigentes:
            dirigentes.append(dirigente.obtenerAtributos())

        ligas = Liga.objects.filter(federacion=self)
        for liga in ligas:
            connection.set_tenant(liga)
            dirigentes += liga.atributos_dirigentes()

        return dirigentes

class Liga(ResolucionReconocimiento):

    def ejecutar_consulta(self, ajustar, consulta):
        from django.db.models import Count, F
        from django.db import connection
        from datetime import date

        from collections import Counter

        from snd.modelos.cafs import CentroAcondicionamiento

        resultado = list()
        clubes = Club.objects.filter(liga=self)
        for i in clubes:
            connection.set_tenant(i)
            resultado += eval(consulta)

        if ajustar:
            resultado = self.ajustar_resultado(resultado)
        return resultado

    def atributos_deportistas(self):
        from snd.modelos.deportistas import Deportista
        from django.db import connection

        deportistas = []

        todos_deportistas = Deportista.objects.filter(entidad=self)

        for i in todos_deportistas:
            deportistas.append(i.obtenerAtributos())

        clubes = Club.objects.filter(liga=self)
        for i in clubes:
            connection.set_tenant(i)
            deportistas += i.atributos_deportistas()

        return deportistas

    def clubes_asociados(self):
        clubes = Club.objects.filter(liga=self)
        return clubes

    def atributos_escenarios(self):
        from snd.modelos.escenarios import Escenario
        from django.db import connection
        escenarios = []

        todos_escenarios = Escenario.objects.filter(entidad=self)
        
        for i in todos_escenarios:
            escenarios.append(i.obtenerAtributos())

        clubes = Club.objects.filter(liga=self)
        for i in clubes:
            connection.set_tenant(i)
            escenarios += i.atributos_escenarios()

        return escenarios

    def atributos_cafs(self):
        from snd.modelos.cafs import CentroAcondicionamiento
        from django.db import connection

        centros = []

        todos_cafs = CentroAcondicionamiento.objects.filter(entidad=self)
        
        for i in todos_cafs:
            centros.append(i.obtenerAtributos())

        clubes = Club.objects.filter(liga=self)
        for i in clubes:
            connection.set_tenant(i)
            centros += i.atributos_cafs()
        
        return centros

    def atributos_personales_apoyo(self):
        from snd.modelos.personal_apoyo import PersonalApoyo
        from django.db import connection

        personales_apoyo = []

        todos_personales_apoyo = PersonalApoyo.objects.filter(entidad=self)

        for i in todos_personales_apoyo:
            personales_apoyo.append(i.obtenerAtributos())

        clubes = Club.objects.filter(liga=self)
        for i in clubes:
            connection.set_tenant(i)
            personales_apoyo += i.atributos_personales_apoyo()

        return personales_apoyo

    def atributos_dirigentes(self):
        from snd.modelos.dirigentes import Dirigente
        from django.db import connection

        dirigentes = []

        todosDirigentes = Dirigente.objects.filter(entidad=self)

        for dirigente in todosDirigentes:
            dirigentes.append(dirigente.obtenerAtributos())

        clubes = Club.objects.filter(liga=self)
        for club in clubes:
            connection.set_tenant(club)
            dirigentes += club.atributos_dirigentes()

        return dirigentes

    def obtener_datos_entidad(self):
        entidad = {
            'tipo_tenant': type(self).__name__,
            'mostrar_info':True,
            'nombre':self.nombre,
            'disciplina': self.disciplina,
            'descripcion': self.descripcion,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'pagina_web': self.pagina_web,
            'disponible_para_transferencias' : self.disponible_para_transferencias()
        }
        return entidad

    federacion = models.ForeignKey(Federacion, null=True, blank=True, verbose_name="federación")
    disciplina = models.ForeignKey(TipoDisciplinaDeportiva)


class Club(ResolucionReconocimiento):
    TIPOS_CLUBES = (
        (1, "Deportivo"),
        (2, "Promotor"),
        (3, "Profesional"),
    )

    liga = models.ForeignKey(Liga, null=True, blank=True)

    def historiales_para_avalar(self,tipo):
        from snd.models import HistorialDeportivo
        return [x.obtener_info_aval() for x in HistorialDeportivo.objects.filter(estado='Pendiente',tipo=tipo,deportista__estado=0)]

    def obtener_datos_entidad(self):
        entidad = {
            'tipo_tenant': type(self).__name__,
            'mostrar_info':True,
            'nombre':self.nombre,
            'disciplina': self.liga.disciplina,
            'descripcion': self.descripcion,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'pagina_web': self.pagina_web,
            'disponible_para_transferencias' : self.disponible_para_transferencias()
        }
        return entidad

class Caf(Entidad):
    pass
    def obtener_datos_entidad(self):
        entidad = {
            'tipo_tenant': type(self).__name__,
            'mostrar_info':True,
            'nombre':self.nombre,
            'disciplina': None,
            'descripcion': self.descripcion,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'pagina_web': self.pagina_web,
            'disponible_para_transferencias' : self.disponible_para_transferencias()
        }
        return entidad

class EscuelaDeportiva_(Entidad):
    disciplina = models.ForeignKey(TipoDisciplinaDeportiva)

    def obtener_datos_entidad(self):
        entidad = {
            'tipo_tenant': type(self).__name__,
            'mostrar_info':True,
            'nombre':self.nombre,
            'disciplina': None,
            'descripcion': self.descripcion,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'pagina_web': self.pagina_web,
            'disponible_para_transferencias' : self.disponible_para_transferencias()
        }
        return entidad


class Nacionalidad(models.Model):
    iso = models.CharField(max_length=5,verbose_name='Abreviacion')
    nombre = models.CharField(max_length=255,verbose_name='pais')

    def __str__(self):
        return self.nombre

class Dias(models.Model):
    nombre = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre


class TipoEscenario(models.Model):
    descripcion = models.CharField(max_length=50, verbose_name='descripción')

    def __str__(self):
        return self.descripcion

class TipoSuperficie(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name='descripción')

    def __str__(self):
        return self.descripcion

class TipoServicioCajaCompensacion(models.Model):
    categoria = models.CharField(max_length=50, verbose_name='categoría')
    descripcion = models.CharField(max_length=100, verbose_name='descripción')

    def __str__(self):
        return self.descripcion

class TipoServicioEscenarioCajaCompensacion(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name='descripción')

    def __str__(self):
        return self.descripcion

class TipoDisciplinaEscenario(models.Model):
    descripcion = models.CharField(max_length=50, verbose_name='descripción')

    def __str__(self):
        return self.descripcion

class TipoUsoEscenario(models.Model):
    descripcion = models.CharField(max_length=50, verbose_name='descripción')

    def __str__(self):
        return self.descripcion

class CaracteristicaEscenario(models.Model):
    descripcion = models.CharField(max_length=50, verbose_name='descripción')

    def __str__(self):
        return self.descripcion
        return self.nombre

class CAClase(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class CAServicio(models.Model):
    nombre = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre

class EPS(models.Model):
    nombre = models.CharField(max_length=300)
    codigo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class CentroBiomedicoServicio(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class EscuelaDeportivaServicio(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre