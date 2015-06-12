#encoding:utf-8

from django.db import models
from entidades.models import Ciudad, Entidad, Nacionalidad, DisciplinaDepostiva
#=======================================================================================================
#Modelos para Entrenadores

class Entrenador(models.Model):
    estado = (
        ('Activo',True),
        ('Inactivo',False),
    )

    tipo_genero = (
        ('Hombre','Hombre'),
        ('Mujer','Mujer'),
    )

    TIPO_IDENTIDAD = (
        ('CED', 'Cédula de ciudadanía'),
        ('CEDEX', 'Cédula de extranjero'),
    )
    estado = models.BooleanField(choices=estado, default=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    genero = models.CharField(choices=tipo_genero,max_length=11)
    foto = models.ImageField(upload_to='fotos_entrenadores', null=True, blank=True)
    tipo_id = models.CharField(max_length=5, choices=TIPO_IDENTIDAD, default='CED')
    nro_id = models.BigIntegerField()
    telefono_fijo = models.CharField(max_length=50, blank=True)
    telefono_celular = models.CharField(max_length=50, blank=True)
    correo_electronico = models.EmailField(blank=True)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.ForeignKey(Nacionalidad)
    ciudad = models.ForeignKey(Ciudad, blank=True)
    #en centimetros
    altura = models.IntegerField(blank=True)
    #en Kg
    peso = models.IntegerField(blank=True)
    entidad_vinculacion = models.ForeignKey(Entidad)

class FormacionDeportiva(models.Model):
    disciplina_deportiva = models.ForeignKey(DisciplinaDepostiva)
    denominacion_diploma = models.CharField(max_length=150)
    nivel = models.CharField(max_length=50, blank=True)
    institucion_formacion = models.CharField(max_length=100)
    pais_formacion = models.ForeignKey(Nacionalidad)
    fecha_comienzo = models.DateField()
    fecha_fin = models.DateField()
    entrenador = models.ForeignKey(Entrenador)


class ExperienciaLaboral(models.Model):
    nombre_cargo = models.CharField(max_length=50)
    institucion = models.CharField(max_length=150)
    fecha_comienzo = models.DateField()
    fecha_fin = models.DateField()
    entrenador = models.ForeignKey(Entrenador)