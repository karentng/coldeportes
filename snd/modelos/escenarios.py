#encoding:utf-8

from entidades.models import *
from django.db import models

class Escenario(models.Model):
    estratos = (
        ('1', 'UNO'),
        ('2', 'DOS'),
        ('3', 'TRES'),
        ('4', 'CUATRO'),
        ('5', 'CINCO'),
        ('6', 'SEIS'),
    )
    ESTADOS = (
        (0,'ACTIVO'),
        (1,'INACTIVO'),
        (2,'EN TRANSFERENCIA'),
        (3,'TRANSFERIDO'),
    )
    DIVISIONES = (
        ('CP','CENTRO POBLADO'),
        ('ZR','ZONA RURAL'),
        ('ZU','ZONA URBANA'),
    )
    nombre =  models.CharField(max_length=100,unique=True)
    direccion = models.CharField(max_length=100, verbose_name='dirección')
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    altura = models.PositiveIntegerField(null=True, blank=True)
    comuna = models.PositiveIntegerField()
    barrio = models.CharField(max_length=20)
    nombre_administrador = models.CharField(max_length=50)
    estrato = models.CharField(choices=estratos, max_length=1)
    entidad = models.ForeignKey(Entidad)    
    estado = models.IntegerField(choices=ESTADOS, verbose_name="estado del Escenario")
    ciudad = models.ForeignKey(Ciudad)
    division_territorial = models.CharField(choices=DIVISIONES, max_length=2, verbose_name="división territorial")    
    descripcion = models.CharField(max_length=1024, verbose_name='descripción', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ("view_escenario", "Permite ver escenario"),
        )

    def fotos(self):
        return [x.foto for x in Foto.objects.filter(escenario=self)]

    def caracteristicas(self):
        return CaracterizacionEscenario.objects.get(escenario=self)

    def capacidad(self):
        return self.caracteristicas().capacidad_espectadores

    def tipo_escenario(self):
        return self.caracteristicas().tipo_escenario

    def posicionInicialMapa(self):
        if self.latitud != None and self.longitud != None:
            coordenadas = [self.latitud, self.longitud]
        else:
            try:
                ciudad = self.ciudad
            except Exception:
                ciudad = Ciudad.objects.get(nombre="Bogotá D.C.")

            coordenadas = [ciudad.latitud, ciudad.longitud]

        return coordenadas

    def obtener_atributos(self):
        from django.conf import settings
        imagen = None
        if len(self.fotos()) != 0:
            imagen = ("%s%s")%(settings.MEDIA_URL, self.fotos()[0].__str__())
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

    def __str__(self):
        return self.nombre


class CaracterizacionEscenario(models.Model):   
    ACCESOS = (
        ('pr', 'PRIVADO'),
        ('dul', 'DE USO LIBRE'),
        ('pcp', 'PÚBLICO CON PAGO'),
    )
    ESTADOS_FISICOS = (
        ('bu', 'BUENO'),
        ('re', 'REGULAR'),
        ('ma', 'MALO'),
    )
    PROPIETARIOS = (
        ('of', 'OFICIAL'),
        ('pr', 'PRIVADO'),
    )
    escenario = models.ForeignKey(Escenario)
    metros_construidos = models.CharField(max_length=50, verbose_name='metros cuadrados construídos')
    caracteristicas = models.ManyToManyField(CaracteristicaEscenario)
    tipo_escenario = models.ForeignKey(TipoEscenario)
    tipo_superficie_juego = models.ManyToManyField(TipoSuperficie)
    clase_acceso = models.CharField(choices=ACCESOS, max_length=3, verbose_name='tipo de acceso') 
    tipo_disciplinas = models.ManyToManyField(TipoDisciplinaDeportiva)
    estado_fisico = models.CharField(choices=ESTADOS_FISICOS, max_length=2, verbose_name='estado físico')
    capacidad_espectadores = models.PositiveIntegerField(verbose_name='capacidad de zona espectadores')
    espectadores_habituales = models.PositiveIntegerField(verbose_name='cantidad de espectadores habituales')
    clase_uso = models.ManyToManyField(TipoUsoEscenario)
    tipo_propietario = models.CharField(max_length=2, verbose_name='tipo de propietario', choices=PROPIETARIOS)
    descripcion = models.TextField(verbose_name='descripción',  max_length=1024, null=True)
    tiene_planos = models.BooleanField(verbose_name='¿Se cuenta con los planos del escenario?', default=False)
    plano_archivo = models.FileField(upload_to="archivos_escenarios/", verbose_name="Plano del escenario (opcional)", null=True, blank=True)
    ficha_catastral = models.FileField(upload_to="archivos_escenarios/", verbose_name="Ficha catastral (opcional)", null=True, blank=True)
    certificado_tradicio_libertad = models.FileField(upload_to="archivos_escenarios/", verbose_name="Certificado de tradición y libertad (opcional)", null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class HorarioDisponibilidad(models.Model):
    escenario = models.ForeignKey(Escenario)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    dias = models.ManyToManyField(Dias, verbose_name='días')
    descripcion = models.TextField(max_length=1024, verbose_name='descripción')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

def ruta_fotos_escenarios(instance, filename):
    return "snd/fotos/escenarios/%s"%(filename.encode('ascii','ignore').decode('ascii'))

class Foto(models.Model):
    escenario = models.ForeignKey(Escenario)
    titulo = models.CharField(max_length=255, verbose_name="título")
    foto = models.ImageField(upload_to=ruta_fotos_escenarios, null=True, blank=True)
    descripcion_foto = models.TextField(blank=True, null=True, max_length=1024, verbose_name='descripción')
    fecha_creacion = models.DateTimeField(auto_now_add=True)


class Video(models.Model):
    escenario = models.ForeignKey(Escenario)
    url = models.CharField(max_length=1024, verbose_name='url', null=True)
    descripcion_video = models.CharField(max_length=1024, null=True, verbose_name="descripción")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Mantenimiento(models.Model):

    PERIODICIDADES = (
        ('di', 'DIARIA'),
        ('se', 'SEMANAL'),
        ('qu', 'QUINCENAL'),
        ('me', 'MENSUAL'),
        ('bm', 'BIMESTRAL'),
        ('tm', 'TRIMESTRAL'),
        ('sm', 'SEMESTRAL'),
        ('an', 'ANUAL'),
    )
    escenario = models.ForeignKey(Escenario)
    fecha_ultimo_mantenimiento = models.DateField( verbose_name="fecha del último mantenimiento", null=True, blank=True)
    descripcion_ultimo_mantenimiento = models.TextField(null=True, blank=True, max_length=1024, verbose_name='descripción del último mantenimiento')
    periodicidad = models.CharField(choices=PERIODICIDADES, max_length=2, null=True, blank=True)    
    razones_no_mantenimiento = models.TextField(null=True, blank=True, max_length=1024, verbose_name="Si no se realiza mantenimiento, mencione las razones")
    tiene_planos = models.BooleanField(verbose_name='¿se cuenta con los planos del escenario?')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class DatoHistorico(models.Model):
    escenario = models.ForeignKey(Escenario)
    fecha_inicio = models.DateField(verbose_name="fecha inicio del suceso histórico")
    fecha_fin = models.DateField(null=True, blank=True)
    descripcion = models.TextField(max_length=1024, verbose_name="descripción del suceso histórico")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Contacto(models.Model):
    escenario = models.ForeignKey(Escenario)
    nombre =  models.CharField(max_length=50)
    telefono = models.CharField(max_length=20, verbose_name='teléfono')
    email = models.EmailField()
    descripcion = models.TextField(max_length=1024, null=True, verbose_name='descripción')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
