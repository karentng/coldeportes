from django.db import models
from tenant_schemas.models import TenantMixin
from coldeportes.utilities import permisos_de_tipo
from django.contrib.auth.models import Group

TIPOS = (
    (1, 'Liga'),
    (2, 'Federación'),
    (3, 'Club'),
    (4, 'Cajas Compensación'),
    (5, 'Ente (Municipal y Departamental)'),
    (6, 'Comité'),
    (7, 'Federación Paralimpica'),
    (8, 'Liga Paralimpica'),
    (9, 'Club Paralimpico'),
    (10,'Centro Acondicionamiento'),
    (11,'Escuela Formación Deportiva'),
)

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
    deporte = models.ForeignKey(TipoDisciplinaDeportiva)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(verbose_name='descripción', blank=True)
    general = models.TextField(verbose_name='general', blank=True)

    def __str__(self):
        if self.general:
            return '('+self.general+')-'+self.nombre
        return self.nombre

class CategoriaDisciplinaDeportiva(models.Model):
    deporte = models.ForeignKey(TipoDisciplinaDeportiva)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(verbose_name='descripción', blank=True)
    general = models.TextField(verbose_name='general', blank=True)

    def __str__(self):
        if self.general:
            return '('+self.general+')-'+self.nombre
        return self.nombre

class Actores(models.Model):
    centros = models.BooleanField(verbose_name="Centros de Acondicionamiento Físico", default=False)
    escenarios = models.BooleanField(verbose_name="Escenarios", default=False)
    deportistas = models.BooleanField(verbose_name="Deportistas", default=False)
    personal_apoyo = models.BooleanField(verbose_name="Personal de apoyo", default=False)
    dirigentes = models.BooleanField(verbose_name="Dirigentes", default=False)
    cajas = models.BooleanField(verbose_name="Cajas de Compensación", default=False)
    selecciones = models.BooleanField(verbose_name="Selecciones", default=False)
    centros_biomedicos = models.BooleanField(verbose_name="Centros Biomédicos", default=False)
    normas = models.BooleanField(verbose_name="Normograma", default=False)
    escuelas_deportivas = models.BooleanField(verbose_name="Escuelas de Formación Deportiva", default=False)
    noticias = models.BooleanField(verbose_name="Noticias", default=False)
    publicidad = models.BooleanField(verbose_name="Publicidad", default=True)

    def resumen(self):
        actores = []
        campos = self._meta.fields
        for i in campos:
            if getattr(self, i.name) == True and i.name != 'id':
                actores.append(i.verbose_name)
        return actores

    def resumen_nombre_atributos(self):
        actores = []
        campos = self._meta.fields
        for i in campos:
            if getattr(self, i.name) == True and i.name != 'id':
                actores.append(i.name)
        return actores

class Entidad(TenantMixin): # Entidad deportiva
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255, verbose_name="dirección")
    pagina_web = models.URLField(verbose_name="página web propia", blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad)
    telefono = models.CharField(max_length=255, verbose_name="teléfono", blank=True)
    descripcion = models.TextField(verbose_name="descripción", blank=True, null=True)

    tipo = models.IntegerField(choices=TIPOS)
    actores = models.OneToOneField(Actores, null=True)
    auto_create_schema = True

    def obtener_padre(self):
        return None

    #def ajustar_resultado(self, resultado, resultado_consulta):
    def ajustar_resultado(self, resultado, campo='descripcion'):
        datos = {}
        for i in resultado:
            try:
                descripcion = i[campo]
            except Exception:
                continue
            if descripcion in datos:
                datos[descripcion] += i['cantidad']
            else:
                datos[descripcion] = i['cantidad']
        return datos

    def ejecutar_consulta(self, ajustar, consulta):
        from django.db.models import Count, F
        from snd.modelos.cafs import CentroAcondicionamiento
        from snd.modelos.escenarios import Escenario
        from snd.modelos.deportistas import HistorialDeportivo,InformacionAdicional,Deportista,InformacionAcademica
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

    #def deportistas_registrables(self):#Revisar
    #    return permisos_de_tipo(self,[3,9])

    def disponible_para_transferencias(self):
        return permisos_de_tipo(self,[3,9])

    #def seleccionable(self):#Revisar
    #    return permisos_de_tipo(self,[1,2,6,7,8])

    def avalable(self):
        return permisos_de_tipo(self,[1,2,7,8])

    def atributos_escenarios(self):
        from snd.modelos.escenarios import Escenario
        todosEscenarios = Escenario.objects.filter(estado=0,entidad=self)
        return len(todosEscenarios)

    def atributos_cafs(self):
        from snd.modelos.cafs import CentroAcondicionamiento
        todosCentros = CentroAcondicionamiento.objects.filter(estado=0, entidad=self)
        return len(todosCentros)

    def atributos_deportistas(self):
        from snd.modelos.deportistas import Deportista
        todos_deportistas = Deportista.objects.filter(estado__in=[0,2], entidad=self)
        return len(todos_deportistas)

    def atributos_personales_apoyo(self):
        from snd.modelos.personal_apoyo import PersonalApoyo
        todos_personales_apoyo = PersonalApoyo.objects.filter(estado=0, entidad=self)
        return len(todos_personales_apoyo)

    def atributos_dirigentes(self):
        from snd.modelos.dirigentes import Dirigente
        todos_dirigentes = Dirigente.objects.filter(estado=0, entidad=self)
        return len(todos_dirigentes)

    def atributos_cajas(self):
        from snd.modelos.cajas_compensacion import CajaCompensacion
        todas_cajas = CajaCompensacion.objects.filter(estado=0, entidad=self)
        return len(todas_cajas)

    def atributos_centros_biomedicos(self):
        from snd.modelos.centro_biomedico import CentroBiomedico
        todos_centros = CentroBiomedico.objects.filter(estado=0, entidad=self)
        return len(todos_centros)

    def atributos_escuelas_deportivas(self):
        from snd.modelos.escuela_deportiva import EscuelaDeportiva
        todos_escuelas = EscuelaDeportiva.objects.filter(estado=0,entidad=self)
        return len(todos_escuelas)

    def atributosDeSusActores(self):
        from django.db import connection
        def agregarActor(datos, perm, identificador, metodo, perms):
            if perm in perms:
                datos[identificador] = metodo()
            connection.set_tenant(self)
            return datos

        tenant = self.obtenerTenant()
        #actores = tenant.actores
        perms = [x.codename for x in Group.objects.get(name='Solo lectura').permissions.all()]
        datos = {}
        datos = agregarActor(datos, 'view_centroacondicionamiento', "caf", tenant.atributos_cafs, perms)
        datos = agregarActor(datos, 'view_escenario', "escenarios", tenant.atributos_escenarios, perms)
        datos = agregarActor(datos, 'view_deportista', "deportistas", tenant.atributos_deportistas, perms)
        datos = agregarActor(datos, 'view_personalapoyo', "personales", tenant.atributos_personales_apoyo, perms)
        datos = agregarActor(datos, 'view_dirigente', "dirigentes", tenant.atributos_dirigentes, perms)
        datos = agregarActor(datos, 'view_cajacompensacion', "cajas", tenant.atributos_cajas, perms)
        datos = agregarActor(datos, 'view_centrobiomedico', "centros_biomedicos", tenant.atributos_centros_biomedicos, perms)
        datos = agregarActor(datos, 'view_escueladeportiva', "escuelas_deportivas", tenant.atributos_escuelas_deportivas, perms)

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
                cantidad = atributosActores[identificador]
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
        definirElementosDashBoard(datos, "escuelas_deportivas", "Escuelas de Formación Deportiva ", "orange", "escuela_deportiva_listar","ion-ios-body")
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

    def obtener_padre(self):
        return self.comite

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

    def obtener_padre(self):
        return self.federacion

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
    DISCAPACIDADES = (
        (1,'Limitaciones Fisicas'),
        (2,'Limitación Auditiva'),
        (3,'Limitación Visual'),
        (4,'Parálisis Cerebral'),
        (5,'Limitación Intelectual'),
    )
    discapacidad = models.IntegerField(choices=DISCAPACIDADES)
    disciplinas = models.ManyToManyField(TipoDisciplinaDeportiva,blank=True)
    liga = models.ForeignKey(LigaParalimpica, null=True, blank=True)

    def obtener_padre(self):
        return self.liga

    def historiales_para_avalar(self,tipo):
        from snd.models import HistorialDeportivo
        return [x.obtener_info_aval() for x in HistorialDeportivo.objects.filter(estado='Pendiente',tipo=tipo,deportista__estado=0)]

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

class Federacion(ResolucionReconocimiento):
    disciplina = models.ForeignKey(TipoDisciplinaDeportiva)
    comite = models.ForeignKey(Comite)

    def obtener_padre(self):
        return self.comite

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
        return len(ligas)

    def atributos_escenarios(self):
        from snd.modelos.escenarios import Escenario
        from django.db import connection
        escenarios = 0

        todosEscenarios = Escenario.objects.filter(estado=0, entidad=self)
        
        escenarios += len(todosEscenarios)

        ligas = Liga.objects.filter(federacion=self)
        for i in ligas:
            connection.set_tenant(i)
            escenarios += i.atributos_escenarios()

        connection.set_tenant(self)

        return escenarios

    def atributos_cafs(self):
        from snd.modelos.cafs import CentroAcondicionamiento
        from django.db import connection

        centros = 0

        todos_cafs = CentroAcondicionamiento.objects.filter(estado=0, entidad=self)
        
        centros += len(todos_cafs)

        ligas = Liga.objects.filter(federacion=self)
        for i in ligas:
            connection.set_tenant(i)
            centros += i.atributos_cafs()

        connection.set_tenant(self)
        
        return centros

    def atributos_deportistas(self):
        from snd.modelos.deportistas import Deportista
        from django.db import connection

        deportistas = 0

        todos_deportistas = Deportista.objects.filter(estado__in=[0,2], entidad=self)

        deportistas += len(todos_deportistas)

        ligas = Liga.objects.filter(federacion=self)
        for i in ligas:
            connection.set_tenant(i)
            deportistas += i.atributos_deportistas()

        connection.set_tenant(self)

        return deportistas

    def atributos_personales_apoyo(self):
        from snd.modelos.personal_apoyo import PersonalApoyo
        from django.db import connection

        personales_apoyo = 0

        todos_personales_apoyo = PersonalApoyo.objects.filter(estado=0, entidad=self)

        personales_apoyo += len(todos_personales_apoyo)

        ligas = Liga.objects.filter(federacion=self)
        for i in ligas:
            connection.set_tenant(i)
            personales_apoyo += i.atributos_personales_apoyo()

        connection.set_tenant(self)

        return personales_apoyo

    def atributos_dirigentes(self):
        from snd.modelos.dirigentes import Dirigente
        from django.db import connection

        dirigentes = 0

        todosDirigentes = Dirigente.objects.filter(estado=0, entidad=self)

        dirigentes += len(todosDirigentes)

        ligas = Liga.objects.filter(federacion=self)
        for liga in ligas:
            connection.set_tenant(liga)
            dirigentes += liga.atributos_dirigentes()

        connection.set_tenant(self)

        return dirigentes

class Liga(ResolucionReconocimiento):

    def ejecutar_consulta(self, ajustar, consulta):
        from django.db.models import Count, F
        from django.db import connection
        from datetime import date

        from collections import Counter

        from snd.modelos.cafs import CentroAcondicionamiento
        from snd.modelos.deportistas import HistorialDeportivo,InformacionAdicional,Deportista,InformacionAcademica

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

        deportistas = 0

        todos_deportistas = Deportista.objects.filter(estado__in=[0,2], entidad=self)

        deportistas += len(todos_deportistas)

        clubes = Club.objects.filter(liga=self)
        for i in clubes:
            connection.set_tenant(i)
            deportistas += i.atributos_deportistas()

        connection.set_tenant(self)

        return deportistas

    def clubes_asociados(self):
        clubes = Club.objects.filter(liga=self)
        return len(clubes)

    def atributos_escenarios(self):
        from snd.modelos.escenarios import Escenario
        from django.db import connection
        escenarios = 0

        todos_escenarios = Escenario.objects.filter(estado=0, entidad=self)

        escenarios += len(todos_escenarios)

        clubes = Club.objects.filter(liga=self)
        for i in clubes:
            connection.set_tenant(i)
            escenarios += i.atributos_escenarios()

        connection.set_tenant(self)

        return escenarios

    def atributos_cafs(self):
        from snd.modelos.cafs import CentroAcondicionamiento
        from django.db import connection

        centros = 0

        todos_cafs = CentroAcondicionamiento.objects.filter(estado=0, entidad=self)
        
        centros += len(todos_cafs)

        clubes = Club.objects.filter(liga=self)
        for i in clubes:
            connection.set_tenant(i)
            centros += i.atributos_cafs()
        
        connection.set_tenant(self)

        return centros

    def atributos_personales_apoyo(self):
        from snd.modelos.personal_apoyo import PersonalApoyo
        from django.db import connection

        personales_apoyo = 0

        todos_personales_apoyo = PersonalApoyo.objects.filter(estado=0, entidad=self)

        personales_apoyo += len(todos_personales_apoyo)

        clubes = Club.objects.filter(liga=self)
        for i in clubes:
            connection.set_tenant(i)
            personales_apoyo += i.atributos_personales_apoyo()

        connection.set_tenant(self)

        return personales_apoyo

    def atributos_dirigentes(self):
        from snd.modelos.dirigentes import Dirigente
        from django.db import connection

        dirigentes = 0

        todosDirigentes = Dirigente.objects.filter(estado=0, entidad=self)

        dirigentes += len(todosDirigentes)

        clubes = Club.objects.filter(liga=self)
        for club in clubes:
            connection.set_tenant(club)
            dirigentes += club.atributos_dirigentes()

        connection.set_tenant(self)

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

    def obtener_padre(self):
        return self.federacion

    federacion = models.ForeignKey(Federacion, null=True, blank=True, verbose_name="federación")
    disciplina = models.ForeignKey(TipoDisciplinaDeportiva)


class SocioClub(models.Model):

    TIPO_IDENTIDAD = (
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
    )

    tipo_documento = models.CharField(max_length=5, choices=TIPO_IDENTIDAD, verbose_name="Tipo de identificación")
    numero_documento = models.CharField(max_length=20, verbose_name="Número de documento", unique=True)
    nombre = models.CharField(max_length=255, verbose_name="Nombres")
    apellido = models.CharField(max_length=255, verbose_name="Apellidos")
    correo = models.EmailField(max_length=255, blank=True, verbose_name="Correo electrónico")
    ciudad = models.ForeignKey(Ciudad)
    empresa = models.CharField(max_length=255, blank=True, verbose_name="Empresa")
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + self.apellido



class PlanesDeCostoClub(models.Model):
    ESTADO = (
        (1, 'Activo'),
        (0, 'Inactivo')
    )
    nombre=models.CharField(max_length=200)
    precio=models.IntegerField()
    descripcion = models.TextField(verbose_name="descripción")
    estado =models.IntegerField(choices=ESTADO, default=1)

    def __str__(self):
        return self.nombre


class Club(ResolucionReconocimiento):
    TIPOS_CLUBES = (
        (0, "Deportivo"),
        (1, "Promotor"),
        (2, "Profesional"),
    )

    liga = models.ForeignKey(Liga, null=True, blank=True)
    disciplina = models.ForeignKey(TipoDisciplinaDeportiva)
    socios = models.ManyToManyField(SocioClub, blank=True);
    planes_de_costo = models.ManyToManyField(PlanesDeCostoClub, blank=True)
    tipo_club = models.IntegerField(choices=TIPOS_CLUBES, default=0)

    def obtener_padre(self):
        return self.liga

    def historiales_para_avalar(self,tipo):
        from snd.models import HistorialDeportivo
        return [x.obtener_info_aval() for x in HistorialDeportivo.objects.filter(estado='Pendiente',tipo=tipo,deportista__estado=0)]

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
            'disponible_para_transferencias' : self.disponible_para_transferencias(),
            'socios': self.socios.all(),
            'planes_de_costo': self.planes_de_costo.all()
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
            'disciplina': self.disciplina,
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


class Permisos(models.Model):
    ACTORES = (
        (1, '--'),
        (2, 'O'),
        (3, 'X'),
        (4, 'X %'),
        (5, '-- %'),
    )
    entidad = models.IntegerField()
    tipo = models.IntegerField()
    centros = models.IntegerField(choices=ACTORES, default=1)
    escenarios = models.IntegerField(choices=ACTORES, default=1)
    deportistas = models.IntegerField(choices=ACTORES, default=1)
    personal_apoyo = models.IntegerField(choices=ACTORES, default=1)
    dirigentes = models.IntegerField(choices=ACTORES, default=1)
    cajas = models.IntegerField(choices=ACTORES, default=1)
    selecciones = models.IntegerField(choices=ACTORES, default=1)
    centros_biomedicos = models.IntegerField(choices=ACTORES, default=1)
    normas = models.IntegerField(choices=ACTORES, default=1)
    escuelas_deportivas = models.IntegerField(choices=ACTORES, default=1)
    noticias = models.IntegerField(choices=ACTORES, default=1)
    publicidad = models.IntegerField(choices=ACTORES, default=2)

    class Meta:
        unique_together = ('entidad','tipo',)

    def get_actores(self,opcion):
        if opcion == 'O':
            opcion = [2]
        elif opcion == 'X':
            opcion = [3,4]
        elif opcion == '%':
            opcion = [4,5]
        elif opcion == '--':
            opcion = [1,5]

        actores_seleccionados = []
        actores = ['centros','escenarios','deportistas','personal_apoyo','dirigentes','cajas','selecciones','centros_biomedicos','normas','escuelas_deportivas','noticias','publicidad']
        for actor in actores:
            if getattr(self,actor) in opcion:
                actores_seleccionados.append(actor)
        return(actores_seleccionados)
