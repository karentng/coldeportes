from django.db import models
from entidades.models import *

def ruta_juegos_imagenes(instance, filename):
    return "juegos/imagenes/%s"%(filename.encode('ascii','ignore').decode('ascii'))


class Juego(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='nombre')
    anio = models.PositiveIntegerField(verbose_name="Año")
    imagen = models.FileField(upload_to=ruta_juegos_imagenes, blank=True, null=True, verbose_name="imagen o logo del juego")
    pais = models.ForeignKey(Nacionalidad, default=52, verbose_name="País")
    descripcion = models.TextField(null=True, blank=True)

    
    def __str__(self):
        return self.nombre

class Competencia(models.Model):
    TIPOS_PARTICIPANTES = (
        (1, "Individual"),
        (2, "Equipos"),
    )
    TIPOS_COMPETENCIAS = (
        (1, "Olímpica"),
        (2, "Paralímpica"),
    )
    
    nombre = models.CharField(max_length=255, verbose_name='nombre')
    fecha_competencia = models.DateField(verbose_name="Fecha de la compentencia")
    tipo_competencia = models.IntegerField(choices=TIPOS_COMPETENCIAS, verbose_name="tipo de competencia")
    tipo_registro = models.IntegerField()
    lugar = models.CharField(max_length=150)
    tipos_participantes = models.IntegerField(choices=TIPOS_PARTICIPANTES, verbose_name="tipo de participantes")
    disciplina_deportiva = models.ForeignKey(TipoDisciplinaDeportiva)
    categoria = models.ForeignKey(CategoriaDisciplinaDeportiva,null=True,blank=True,verbose_name='Categoría')
    modalidad = models.ForeignKey(ModalidadDisciplinaDeportiva,null=True,blank=True,verbose_name='Modalidad de competencia')
    sets = models.BooleanField(verbose_name="¿Requiere el registro de varios sets?")
    descripcion = models.TextField(null=True, blank=True)
    juego = models.ForeignKey(Juego)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='nombre')
    competencia = models.ForeignKey(Competencia)
    departamento = models.ForeignKey(Departamento)
    posicion = models.IntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

class Participante(models.Model):
    GENEROS = (
        ('HOMBRE','MASCULINO'),
        ('MUJER','FEMENINO'),
    )

    nombres = models.CharField(max_length=255, verbose_name='nombre')
    apellidos = models.CharField(max_length=255, verbose_name='apellidos')
    genero = models.CharField(max_length=11, choices=GENEROS, verbose_name='Género del deportista')
    categoria = models.ForeignKey(CategoriaDisciplinaDeportiva)
    departamento = models.ForeignKey(Departamento)
    posicion = models.IntegerField(default=0)
    tiempo = models.TimeField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    equipo = models.ForeignKey(Equipo, null=True, blank=True)
    competencia = models.ForeignKey(Competencia, null=True, blank=True)