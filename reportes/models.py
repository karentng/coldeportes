from django.db import models
from entidades.models import *
from snd.modelos.escenarios import *


class TenantEscenarioView(models.Model):
    class Meta:
        managed = False
    #campos modelo escenario
    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    latitud = models.FloatField(max_length=10)
    longitud = models.FloatField(max_length=10)
    altura = models.PositiveIntegerField()
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.PositiveIntegerField()
    barrio = models.CharField(max_length=20)
    estrato = models.CharField(max_length=1)
    nombre_administrador = models.CharField(max_length=50, null=True)
    entidad = models.ForeignKey(Entidad)
    estado = models.IntegerField()
    division_territorial = models.CharField(max_length=2)
    descripcion_escenario = models.CharField(max_length=1024, null=True)
    fecha_creacion_escenario = models.DateTimeField()
    #campos modelo caracterizacion
    tipo_escenario = models.ForeignKey(TipoEscenario)
    tipodisciplinadeportiva = models.ForeignKey(TipoDisciplinaDeportiva)
    estado_fisico = models.CharField(max_length=2)
    tiposuperficie = models.ForeignKey(TipoSuperficie)
    tipo_propietario = models.CharField(max_length=2)
    clase_acceso = models.CharField(max_length=3)
    capacidad_espectadores = models.CharField(max_length=50, verbose_name='capacidad de zona espectadores')
    caracteristicaescenario = models.ForeignKey(CaracteristicaEscenario)


    #campos modelo contacto
    nombre_contacto =  models.CharField(max_length=50)
    telefono_contacto = models.CharField(max_length=20)
    email_contacto = models.EmailField()
    descripcion_contacto = models.CharField(max_length=1024, null=True)
    #campos modelo horario
    horario_id = models.IntegerField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    dias = models.ForeignKey(Dias)
    descripcion_horario = models.CharField(max_length=1024)
    #campos modelo Foto
    foto = models.ImageField(upload_to='fotos_escenarios', null=True, blank=True)
    #campos mantenimiento
    periodicidad = models.CharField(max_length=2, null=True, blank=True)

    def obtener_atributos(self):
        from django.conf import settings
        imagen = None
        if self.foto != None:
            imagen = ("%s%s")%(settings.MEDIA_URL, self.foto.__str__())
        else:
            imagen = ("%s%s")%(settings.STATIC_URL, "img/actores/EscenarioView.PNG")
        atributos = [
            ["Nombre", self.nombre],
            ["Ciudad", self.ciudad.nombre],
            ["Comuna", self.comuna],
            ["Barrio", self.barrio],
            ["Estrato", self.estrato],
            ["Dirección", self.direccion],
            ["Latitud", self.latitud],
            ["Longitud", self.longitud],
        ]
        return [imagen, atributos, self.latitud, self.longitud, "Escenario!"]

def ruta_fotos_cafs(instance, filename):
    return "snd/fotos/cafs/%s-%s"%(instance.id, filename.encode('ascii','ignore').decode('ascii'))

class TenantCafView(models.Model):
    class Meta:
        managed = False

    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, verbose_name="dirección")
    telefono = models.CharField(max_length=50, verbose_name="teléfono")
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.PositiveIntegerField()
    estrato = models.PositiveIntegerField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    email = models.EmailField()
    web = models.URLField(verbose_name="página web")
    altura = models.PositiveIntegerField()
    estado = models.IntegerField()
    entidad = models.ForeignKey(Entidad)
    fecha_creacion = models.DateTimeField()
    nombre_clase = models.CharField(max_length=255)
    nombre_servicio = models.CharField(max_length=255)
    foto = models.ImageField(upload_to=ruta_fotos_cafs, null=True, blank=True)
    barrio = models.CharField(max_length=20)

    def obtener_atributos(self):
        from django.conf import settings
        imagen = None
        if self.foto != None:
            imagen = ("%s%s")%(settings.MEDIA_URL, self.foto.__str__())
        else:
            imagen = ("%s%s")%(settings.STATIC_URL, "img/actores/CAFView.PNG")

        atributos = [
            ["Nombre", self.nombre],
            ["Ciudad", self.ciudad.nombre],
            ["Comuna", self.comuna],
            ["Barrio", self.barrio],
            ["Estrato", self.estrato],
            ["Dirección", self.direccion],
            ["Teléfono", self.telefono],
            ["Latitud", self.latitud],
            ["Longitud", self.longitud],
        ]

        return [imagen, atributos, self.latitud, self.longitud, "CAF!"]

class TenantPersonalApoyoView(models.Model):
    ACTIVIDADES = (
        (0,'MÉDICO DEPORTÓLOGO'),
        (1,'FISIOTERAPEUTA'),
        (2,'PSICÓLOGO DEPORTIVO'),
        (3,'NUTRICIONISTA'),
        (4,'QUINESIÓLOGO'),
        (5,'QUIROPRÁCTICO'),
        (6,'PREPARADOR FÍSICO'),
        (7,'TRABAJADOR SOCIAL'),
        (8,'FISIÓLOGO'),
        (9,'BIOMECÁNICO'),
        (10,'METODÓLOGO'),
        (11,'ENTRENADOR'),
        (12,'MONITOR'),
        (13,'ENTRENADOR PERSONALIZADO'),
        (14,'ANIMADOR SOCIOCULTURAL'),
        (15,'RECREADOR'),
        (16,'PROMOTOR DE ACTIVIDAD FÍSICA'),
    )

    class Meta:
        managed = False

    actividad = models.IntegerField(choices=ACTIVIDADES)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    entidad = models.ForeignKey(Entidad)
    genero = models.CharField(max_length=11)
    tipo_id = models.CharField(max_length=5)
    identificacion = models.CharField(max_length=100,verbose_name='Identificación')
    fecha_nacimiento = models.DateField()
    nacionalidad = models.ForeignKey(Nacionalidad)
    ciudad = models.ForeignKey(Ciudad)
    etnia = models.CharField(max_length=20)
    lgtbi = models.BooleanField()
    fecha_creacion = models.DateField()
    estado = models.IntegerField()
    nivel_formacion = models.CharField(max_length=20)
    estado_formacion = models.CharField(max_length=20)
    fecha_finalizacion = models.IntegerField()

class TenantDeportistaView(models.Model):

    class Meta:
        managed = False

    #campos modelo deportista
    identificacion = models.CharField(max_length=100,verbose_name='Identificación')
    genero = models.CharField(max_length=11)
    ciudad_residencia = models.ForeignKey(Ciudad)
    tipodisciplinadeportiva = models.ForeignKey(TipoDisciplinaDeportiva)
    fecha_nacimiento = models.DateField()
    fecha_creacion = models.DateTimeField()
    lgtbi = models.BooleanField()
    etnia = models.CharField(max_length=20)
    nacionalidad = models.ForeignKey(Nacionalidad)
    estado = models.IntegerField()
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100,verbose_name='Apellidos')
    entidad = models.ForeignKey(Entidad)
    #campos historial deportivo
    tipo_participacion = models.CharField(max_length=100)
    estado_participacion = models.CharField(max_length=50)

    #campos informacion academica
    nivel_formacion = models.CharField(max_length=20)
    estado_formacion = models.CharField(max_length=20)
    fecha_finalizacion = models.IntegerField(blank=True,null=True)

    #campos informacion adicional
    usa_centros_biomedicos = models.BooleanField()
    es_beneficiario_programa_apoyo = models.BooleanField()

    #campos historial lesiones
    tipo_lesion = models.IntegerField()
    periodo_rehabilitacion = models.IntegerField()
    fecha_lesion = models.DateField()
    segmento_corporal = models.IntegerField()

    fecha_participacion = models.DateField()

class TenantDirigenteView(models.Model):

    class Meta:
        managed = False

    identificacion = models.CharField(max_length=100,verbose_name='Identificación')
    fecha_creacion = models.DateTimeField()
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    nacionalidad = models.ForeignKey(Nacionalidad)
    entidad = models.ForeignKey(Entidad)
    estado = models.IntegerField()
    ciudad = models.ForeignKey(Ciudad)
    genero = models.CharField(max_length=11)
    #campos informacion academica
    nivel_formacion = models.CharField(max_length=20)
    estado_formacion = models.CharField(max_length=20)
    fecha_finalizacion = models.IntegerField(blank=True,null=True)

class TenantEscuelaView(models.Model):

    class Meta:
        managed = False

    nombre = models.CharField(max_length=100)
    telefono_fijo = models.CharField(max_length=100)
    tipo_sede = models.CharField(max_length=150)
    email = models.CharField(max_length=100)
    web = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField()
    estado = models.IntegerField()
    ciudad = models.ForeignKey(Ciudad)
    estrato = models.PositiveIntegerField()
    entidad = models.ForeignKey(Entidad)
    nombre_servicio = models.CharField(max_length=255)


class TenantCajasView(models.Model):
    clases = (('G', 'Grande'), ('M', 'Mediana'), ('P', 'Pequeña'), )

    class Meta:
        managed = False

    nombre = models.CharField(max_length=100)
    estado = models.IntegerField()
    ciudad = models.ForeignKey(Ciudad)
    email = models.CharField(max_length=100)
    clasificacion = models.CharField(max_length=100, choices=clases)
    entidad = models.ForeignKey(Entidad)
    nombre_servicio = models.CharField(max_length=255)