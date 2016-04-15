from django.db import models
from entidades.models import *

def ruta_juegos_imagenes(instance, filename):
    return "juegos/imagenes/%s"%(filename.encode('ascii','ignore').decode('ascii'))


class Juego(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='nombre')
    anio = models.PositiveIntegerField(verbose_name="año")
    imagen = models.FileField(upload_to=ruta_juegos_imagenes, blank=True, null=True, verbose_name="imagen o logo del juego")
    pais = models.ForeignKey(Nacionalidad, default=52, verbose_name="País")
    descripcion = models.TextField(null=True, blank=True, verbose_name="descripción")

    
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
    )
    
    nombre = models.CharField(max_length=255, verbose_name='nombre')
    fecha_competencia = models.DateField(verbose_name="fecha de la competencia")
    tipo_competencia = models.IntegerField(choices=TIPOS_COMPETENCIAS, verbose_name="tipo de competencia")
    tipo_registro = models.IntegerField(choices=TIPOS_REGISTROS)
    lugar = models.CharField(max_length=150)
    tipos_participantes = models.IntegerField(choices=TIPOS_PARTICIPANTES, verbose_name="tipo de participantes")
    deporte = models.ForeignKey(TipoDisciplinaDeportiva,verbose_name='Disciplina Deportiva')
    categoria = models.ForeignKey(CategoriaDisciplinaDeportiva,null=True,blank=True,verbose_name='categoría')
    modalidad = models.ForeignKey(ModalidadDisciplinaDeportiva,null=True,blank=True,verbose_name='modalidad de competencia')
    descripcion = models.TextField(null=True, blank=True, verbose_name='descripción')
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
    tiempo = models.CharField(blank=True, null=True, max_length=10, help_text="El tiempo debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05.105")
    puntos = models.IntegerField(default=0, null=True)
    metros = models.DecimalField(default=0, null=True, max_digits=3, decimal_places=2, help_text='En metros')
    departamento = models.ForeignKey(Departamento)
    marca = models.CharField(blank=True, null=True, max_length=10, help_text="La marca debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05")
    posicion = models.IntegerField(default=0, verbose_name="posición")    
    creado = models.DateTimeField(auto_now_add=True)
    competencia = models.ForeignKey(Competencia)
    genero = models.IntegerField(choices=GENEROS, verbose_name='género de competidores')




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
    peso = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='peso (kg)', null=True, blank=True)
    posicion = models.IntegerField(default=0, verbose_name="posición")
    metros = models.DecimalField(default=0, null=True, max_digits=4, decimal_places=2, help_text='En metros')
    puntos = models.IntegerField(default=0, null=True)
    tiempo = models.CharField(null=True, max_length=10, help_text="El tiempo debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05.105")
    marca = models.CharField(blank=True, null=True, max_length=10, help_text="La marca debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05")
    equipo = models.ForeignKey(Equipo, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    competencia = models.ForeignKey(Competencia, null=True)