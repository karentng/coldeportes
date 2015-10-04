from django.db import models
from tenant_schemas.models import TenantMixin

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

class Actores(models.Model):
    centros = models.BooleanField(verbose_name="Centros de Acondicionamiento Físico")
    escenarios = models.BooleanField(verbose_name="Escenarios")
    deportistas = models.BooleanField(verbose_name="Deportistas")
    personal_apoyo = models.BooleanField(verbose_name="Personal de apoyo")
    dirigentes = models.BooleanField(verbose_name="Dirigentes")
    cajas = models.BooleanField(verbose_name="Cajas de Compensación")
    selecciones = models.BooleanField(verbose_name="Selecciones")
    centros_biomedicos = models.BooleanField(verbose_name="Centros Biomédicos")

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
        try:
            return modelo.objects.get(id=self.id)
        except Exception:
            return self

    def seleccionable(self):
        if self.tipo in [1,2,6,7,8]:
            return True
        return False

    def avalable(self):
        if self.tipo in [1,2,7,8]:
            return True
        return False

    def atributosDeSusEscenarios(self):
        from snd.modelos.escenarios import Escenario
        todosEscenarios = Escenario.objects.filter(entidad=self)
        escenarios = []
        for i in todosEscenarios:
            escenarios.append(i.obtenerAtributos())
        
        return escenarios

    def atributosDeSusCafs(self):
        from snd.modelos.cafs import CentroAcondicionamiento
        todosCentros = CentroAcondicionamiento.objects.filter(entidad=self)
        centros = []
        for i in todosCentros:
            centros.append(i.obtenerAtributos())
        
        return centros

    def cantidadActoresAsociados(self):
        from snd.models import CentroAcondicionamiento, CajaCompensacion, Deportista, Dirigente, Escenario, PersonalApoyo
        def obtenerTodos(booleano, modelo, nombre, datos, color, url):
            if booleano:
                return datos + [[nombre, color, modelo.objects.all().count(), url]]
            return datos

        datos = []
        actores = self.actores
        datos = obtenerTodos(actores.centros, CentroAcondicionamiento, "CAFs", datos, "red", "listar_cafs")
        datos = obtenerTodos(actores.escenarios, Escenario, "Escenarios", datos, "blue", "listar_escenarios")
        datos = obtenerTodos(actores.deportistas, Deportista, "Deportistas", datos, "orange", "deportista_listar")
        datos = obtenerTodos(actores.personal_apoyo, PersonalApoyo, "Personales de Apoyo", datos, "green", "personal_apoyo_listar")
        datos = obtenerTodos(actores.dirigentes, Dirigente, "Dirigentes", datos, "purple", "dirigentes_listar")
        datos = obtenerTodos(actores.cajas, CajaCompensacion, "Cajas de Compensación", datos, "black", "listar_ccfs")
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

class Comite(Entidad):
    TIPOS_COMITE = (
        (1, 'Comité Olimpico Colombiano'),
        (2, 'Comité Paralímpico Colombiano'),
    )
    tipo_comite = models.IntegerField(choices=TIPOS_COMITE)

    def save(self, *args, **kwargs):
        actores = self.actores
        if actores != None:
            actores.selecciones = True
            actores.save()
        super(Comite, self).save(*args, **kwargs)

class FederacionParalimpica(Entidad):
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

        actores = self.actores
        if actores != None:
            actores.dirigentes = True
            actores.personal_apoyo = True
            actores.selecciones = True
            actores.save()
        super(FederacionParalimpica, self).save(*args, **kwargs)

class LigaParalimpica(Entidad):
    DISCAPACIDADES = (
        (1,'Limitaciones Fisica'),
        (2,'Limitación Auditiva'),
        (3,'Limitación Visual'),
        (4,'Parálisis Cerebral'),
        (5,'Limitación Intelectual'),
    )
    discapacidad = models.IntegerField(choices=DISCAPACIDADES)
    federacion = models.ForeignKey(FederacionParalimpica)

    def save(self, *args, **kwargs):
        actores = self.actores
        if actores != None:
            actores.dirigentes = True
            actores.personal_apoyo = True
            actores.selecciones = True
            actores.save()
        super(LigaParalimpica, self).save(*args, **kwargs)

class ClubParalimpico(Entidad):
    liga = models.ForeignKey(LigaParalimpica, null=True, blank=True)

    def historiales_para_avalar(self,tipo):
        from snd.models import HistorialDeportivo
        return [x.obtener_info_aval() for x in HistorialDeportivo.objects.filter(estado='Pendiente',tipo=tipo,deportista__estado=0)]


    def save(self, *args, **kwargs):
        actores = self.actores
        if actores != None:
            actores.dirigentes = True
            actores.personal_apoyo = True
            actores.save()
        super(ClubParalimpico, self).save(*args, **kwargs)


class CajaDeCompensacion(Entidad):
    pass

class Federacion(Entidad):
    disciplina = models.ForeignKey(TipoDisciplinaDeportiva)
    comite = models.ForeignKey(Comite)

    def save(self, *args, **kwargs):
        comite = Comite.objects.get(tipo_comite=1)
        self.comite=comite

        actores = self.actores
        if actores != None:
            actores.dirigentes = True
            actores.personal_apoyo = True
            actores.selecciones = True
            actores.save()
        super(Federacion, self).save(*args, **kwargs)

    def atributosDeSusEscenarios(self):
        from snd.modelos.escenarios import Escenario
        from django.db import connection
        escenarios = []

        todosEscenarios = Escenario.objects.filter(entidad=self)
        
        for i in todosEscenarios:
            escenarios.append(i.obtenerAtributos())

        ligas = Liga.objects.filter(federacion=self)
        for i in ligas:
            connection.set_tenant(i)
            escenarios += i.atributosDeSusEscenarios()

        return escenarios

    def atributosDeSusCafs(self):
        from snd.modelos.cafs import CentroAcondicionamiento
        from django.db import connection

        centros = []

        todosEscenarios = CentroAcondicionamiento.objects.filter(entidad=self)
        
        for i in todosEscenarios:
            centros.append(i.obtenerAtributos())

        ligas = Liga.objects.filter(federacion=self)
        for i in ligas:
            connection.set_tenant(i)
            centros += i.atributosDeSusCafs()
        
        return centros

class Liga(Entidad):
    federacion = models.ForeignKey(Federacion, null=True, blank=True, verbose_name="federación")
    disciplina = models.ForeignKey(TipoDisciplinaDeportiva)

    def save(self, *args, **kwargs):
        actores = self.actores
        if actores != None:
            actores.dirigentes = True
            actores.personal_apoyo = True
            actores.selecciones = True
            actores.save()
        super(Liga, self).save(*args, **kwargs)

    def atributosDeSusEscenarios(self):
        from snd.modelos.escenarios import Escenario
        from django.db import connection
        escenarios = []

        todosEscenarios = Escenario.objects.filter(entidad=self)
        
        for i in todosEscenarios:
            escenarios.append(i.obtenerAtributos())

        clubes = Club.objects.filter(liga=self)
        for i in clubes:
            connection.set_tenant(i)
            escenarios += i.atributosDeSusEscenarios()

        return escenarios

    def atributosDeSusCafs(self):
        from snd.modelos.cafs import CentroAcondicionamiento
        from django.db import connection

        centros = []

        todosEscenarios = CentroAcondicionamiento.objects.filter(entidad=self)
        
        for i in todosEscenarios:
            centros.append(i.obtenerAtributos())

        clubes = Club.objects.filter(liga=self)
        for i in clubes:
            connection.set_tenant(i)
            centros += i.atributosDeSusCafs()
        
        return centros

class Club(Entidad):
    liga = models.ForeignKey(Liga, null=True, blank=True)

    def historiales_para_avalar(self,tipo):
        from snd.models import HistorialDeportivo
        return [x.obtener_info_aval() for x in HistorialDeportivo.objects.filter(estado='Pendiente',tipo=tipo,deportista__estado=0)]

    def save(self, *args, **kwargs):
        actores = self.actores
        if actores != None:
            actores.dirigentes = True
            actores.personal_apoyo = True
            actores.save()
        super(Club, self).save(*args, **kwargs)


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