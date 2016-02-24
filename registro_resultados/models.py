from django.db import models
from entidades.models import CategoriaDisciplinaDeportiva, Departamento, TipoDisciplinaDeportiva

def ruta_competencias_imagenes(instance, filename):
    return "competencias/imagenes/%s"%(filename.encode('ascii','ignore').decode('ascii'))

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
    fecha_competencia = models.DateTimeField(verbose_name="Fecha de la compentencia")
    tipo_competencia = models.IntegerField(choices=TIPOS_COMPETENCIAS, verbose_name="tipo de competencia")
    tipos_participantes = models.IntegerField(choices=TIPOS_PARTICIPANTES, verbose_name="tipo de participantes")
    disciplina_deportiva = models.ForeignKey(TipoDisciplinaDeportiva)
    tipo_registro = models.IntegerField(verbose_name='Tipo de Registros')
    sets = models.BooleanField(verbose_name="¿Requiere el registro de varios sets?")
    descripcion = models.TextField(null=True, blank=True)
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