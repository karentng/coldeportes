from django.db import models
from entidades.models import *
from django.core.validators import MinValueValidator

def ruta_juegos_imagenes(instance, filename):
    return "juegos/imagenes/%s"%(filename.encode('ascii','ignore').decode('ascii'))


class Juego(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='nombre')
    anio = models.PositiveIntegerField(verbose_name="año")
    imagen = models.FileField(upload_to=ruta_juegos_imagenes, blank=True, null=True, verbose_name="imagen o logo del juego")
    pais = models.ForeignKey(Nacionalidad, default=52, verbose_name="País")
    descripcion = models.TextField(null=True, blank=True, verbose_name="descripción", help_text="Ingrese detalles de como se desarrolló el juego, detalles y demás información que considere pertinente en la descripción del juego.")

    
    def __str__(self):
        return self.nombre+", Año: "+str(self.anio)

class Competencia(models.Model):
    TIPOS_PARTICIPANTES = (
        (1, "Individual"),
        (2, "Equipos"),
    )
    TIPOS_COMPETENCIAS = (
        (1, "Olímpica"),
        (2, "Paralímpica"),
    )
    TIPOS_REGISTROS = (
        (1, "Tiempos"),
        (2, "Puntos"),
        (3, "Metros"),
        (4, "Posición")
    )
    
    nombre = models.CharField(max_length=255, verbose_name='nombre')
    fecha_competencia = models.DateField(verbose_name="fecha de la competencia")
    tipo_competencia = models.IntegerField(choices=TIPOS_COMPETENCIAS, verbose_name="tipo de competencia")
    lugar = models.CharField(max_length=150)
    deporte = models.ForeignKey(TipoDisciplinaDeportiva,verbose_name='Disciplina Deportiva')
    categoria = models.ForeignKey(CategoriaDisciplinaDeportiva,null=True,blank=True,verbose_name='categoría del deporte')
    modalidad = models.ForeignKey(ModalidadDisciplinaDeportiva,null=True,blank=True,verbose_name='modalidad del deporte')
    tipos_participantes = models.IntegerField(choices=TIPOS_PARTICIPANTES, verbose_name="tipo de participantes")
    tipo_registro = models.IntegerField(choices=TIPOS_REGISTROS, verbose_name = "Marcas de la Competencia")
    descripcion = models.TextField(null=True, blank=True, verbose_name='descripción', help_text="Ingrese detalles de como se desarrollo la competencia, detalles y demás información que considere pertinente en la descripción de la competencia.")
    juego = models.ForeignKey(Juego)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    GENEROS = (
        (1,'MASCULINO'),
        (2,'FEMENINO'),
        (3,'MIXTO'),
    )

    nombre = models.CharField(max_length=255, verbose_name='nombre')
    posicion = models.IntegerField(default=0, verbose_name="posición")    
    tiempo = models.CharField(blank=True, null=True, max_length=10, help_text="El tiempo debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05.105")
    puntos = models.IntegerField(default=0, null=True, blank=True)
    metros = models.DecimalField(default=0, null=True, blank=True, max_digits=6, decimal_places=3, help_text='En metros')
    departamento = models.ForeignKey(Departamento)
    marca = models.CharField(blank=True, null=True, max_length=10, help_text="Este campo se refiere al mejor desempeño que tiene el equipo en esta competencia. La marca debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05")
    genero = models.IntegerField(choices=GENEROS, verbose_name='género de competidores')
    creado = models.DateTimeField(auto_now_add=True)
    competencia = models.ForeignKey(Competencia)
    medallas_por_integrantes = models.BooleanField(default = False)
    cantidad_medallas_equipo = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(2)], verbose_name="cantidad de medallas del equipo * ")




class Participante(models.Model):
    GENEROS = (
        (1,'MASCULINO'),
        (2,'FEMENINO'),
    )

    nombre = models.CharField(max_length=255, verbose_name='nombre')
    genero = models.IntegerField(choices=GENEROS, verbose_name='género del deportista')
    departamento = models.ForeignKey(Departamento)
    club = models.CharField(max_length=100, verbose_name='club de Registro', null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    estatura = models.PositiveIntegerField(verbose_name='estatura (cm)', null=True, blank=True)
    peso = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='peso (kg)', null=True, blank=True)
    posicion = models.IntegerField(default=0, verbose_name="posición")
    metros = models.DecimalField(default=0, null=True, blank=True, max_digits=6, decimal_places=3, help_text='En metros')
    puntos = models.IntegerField(default=0, null=True, blank=True)
    tiempo = models.CharField(null=True, blank=True, max_length=10, help_text="El tiempo debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05.105")
    marca = models.CharField(verbose_name = "Mejor Registro", blank=True, null=True, max_length=10, help_text="Este campo se refiere al mejor desempeño que tiene el participante en esta competencia. La marca debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05")
    equipo = models.ForeignKey(Equipo, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    competencia = models.ForeignKey(Competencia, null=True)