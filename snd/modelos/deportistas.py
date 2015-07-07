#encoding:utf-8

from entidades.models import *
from django.db import models


class Deportista(models.Model):
    #Datos personales
        #Identificacion
    tipo_sexo = (
        ('Hombre','Hombre'),
        ('Mujer','Mujer'),
    )
    TIPO_IDENTIDAD = (
        ('TI', 'Tarjeta de Identidad'),
        ('CC', 'Cédula de ciudadanía'),
        ('CCEX', 'Cédula de extranjero'),
        ('PASS', 'Pasaporte'),
    )
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    genero = models.CharField(choices=tipo_sexo,max_length=11, verbose_name='Genero del Deportista',default='Hombre')
    tipo_id = models.CharField(max_length=10, choices=TIPO_IDENTIDAD, default='CC',verbose_name='Tipo de Identificación')
    identificacion = models.CharField(max_length=100,unique=True)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.ManyToManyField(Nacionalidad)
    ciudad_nacimiento = models.ForeignKey(Ciudad,blank=True,null=True)
    barrio = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    telefono = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
        #Entidad
    entidad = models.ForeignKey(Entidad)
        #Disciplina
    disciplinas = models.ManyToManyField(TipoDisciplinaDeportiva)
    activo = models.BooleanField(default=True)
    video = models.URLField(max_length=1024, verbose_name='Video', null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_deportistas', null=True, blank=True)

#Composicion corporal
class ComposicionCorporal(models.Model):
    tipos_rh =(
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('O+','O+'),
        ('O-','O-'),
    )
    tipos_talla_choices = (
        ('Niño','Niño'),
        ('Adulto','Adulto'),
    )
    deportista = models.ForeignKey(Deportista)
    peso = models.FloatField(help_text="En kg", verbose_name="Peso (kg)")
    estatura = models.IntegerField(help_text="En cm", verbose_name="Estatura (cm)")
    RH = models.CharField(max_length=4,choices=tipos_rh,default='O+')
    tipo_talla = models.CharField(max_length=7,choices=tipos_talla_choices,default='Adulto',verbose_name='Talla para')
    talla_camisa = models.CharField(max_length=2)
    talla_pantaloneta = models.CharField(max_length=2)
    talla_zapato = models.CharField(max_length=2)
    porcentaje_grasa = models.CharField(max_length=7)
    porcentaje_musculo = models.CharField(max_length=7)


#Hitorial deportivo
class HistorialDeportivo(models.Model):
    tipo_his_deportivo=(
        ('Competencia','Competencia'),
        ('Logro Deportivo','Logro Deportivo'),
        ('Participacion en Equipo','Participacion en Equipo'),
        ('Premio','Premio'),
    )
    fecha = models.DateField()
    lugar = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1024, verbose_name='descripción', null=True)
    institucion_equipo = models.CharField(max_length=100,blank=True,null=True)
    tipo = models.CharField(choices=tipo_his_deportivo,max_length=100,verbose_name='Tipo Historial',default='Competencia')
    deportista = models.ForeignKey(Deportista)

#Informacion academica
class InformacionAcademica(models.Model):
    tipo_academica = (
        ('Jardin','Jardin'),
        ('Primaria','Primaria'),
        ('Bachillerato','Bachillerato'),
        ('Pregrado','Pregrado'),
        ('Postgrado','Postgrado'),
    )
    tipo_estado = (
        ('Actual','Actual'),
        ('Finalizado','Finalizado'),
        ('Incompleto','Incompleto'),
    )
    pais = models.ForeignKey(Nacionalidad)
    institucion = models.CharField(max_length=100)
    nivel = models.CharField(choices=tipo_academica,max_length=20)
    estado = models.CharField(choices=tipo_estado,max_length=20)
    profesion =  models.CharField(max_length=100,blank=True,null=True)
    grado_semestre = models.IntegerField(verbose_name='Grado o Semestre', null=True, blank=True)
    fecha_finalizacion = models.IntegerField(blank=True,null=True,verbose_name='Año Finalización')
    deportista = models.ForeignKey(Deportista)

