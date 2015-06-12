#encoding:utf-8
from snd.modelos.cafs import *
from snd.modelos.escenarios import *

from django.db import models
from entidades.models import *

#=======================================================================================================
# Gestion de dirigentes

class Dirigente(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    superior = models.ForeignKey('Dirigente', null=True, blank=True); # las comillas fuerza un lazy reference, necesario por la referencia cíclica
    foto = models.ImageField(upload_to='fotos', null=True, blank=True)
    entidad = models.ForeignKey(Entidad, null=True, blank=True)

    def __str__(self):
        return self.nombre

#=======================================================================================================
#Modelos de deportistas
#Informacion del deportista, informacion deportiva

class Deportista(models.Model):
    #Datos personales
        #Identificacion
    tipo_sexo = (
        ('Masculino','Masculino'),
        ('Femenino','Femenino'),
    )
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    sexo = models.CharField(choices=tipo_sexo,max_length=11, verbose_name='Sexo del Deportista')
    identificacion = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.ManyToManyField(Nacionalidad)
    ciudad_nacimiento = models.ForeignKey(Ciudad,blank=True)
    barrio = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    telefono = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
        #Entidad
    entidad = models.ForeignKey(Entidad)
        #Disciplina
    disciplinas = models.ManyToManyField(DisciplinaDepostiva)
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
    deportista = models.ForeignKey(Deportista)
    peso = models.FloatField()
    estatura = models.FloatField()
    RH = models.CharField(max_length=4,choices=tipos_rh)
    talla_camisa = models.CharField(max_length=100)
    talla_pantaloneta = models.CharField(max_length=100)
    talla_zapato = models.CharField(max_length=100)
    porcentaje_grasa = models.CharField(max_length=100)
    porcentaje_musculo = models.CharField(max_length=100)


#Hitorial deportivo
class HistorialDeportivo(models.Model):
    tipo_his_deportivo=(
        ('Competencia','Competencia'),
        ('Premio','Premio'),
        ('Logro Deportivo','Logro Deportivo'),
        ('Participacion en Equipo','Participacion en Equipo'),
    )
    fecha = models.DateField()
    lugar = models.CharField(max_length=100)
    descripcion = models.TextField()
    institucion_equipo = models.CharField(max_length=100,blank=True,null=True)
    tipo = models.CharField(choices=tipo_his_deportivo,max_length=100,verbose_name='Tipo Historial')
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
        ('Finalizado','Finalizado'),
        ('Incompleto','Incompleto'),
        ('Actual','Actual'),
    )
    pais = models.ForeignKey(Nacionalidad)
    institucion = models.CharField(max_length=100)
    nivel = models.CharField(choices=tipo_academica,max_length=20)
    estado = models.CharField(choices=tipo_estado,max_length=20)
    profesion =  models.CharField(max_length=100,blank=True,null=True)
    grado_semestre = models.IntegerField(verbose_name='Grado o Semestre', null=True, blank=True)
    fecha_finalizacion = models.IntegerField(blank=True,null=True,verbose_name='Año Finalización')
    deportista = models.ForeignKey(Deportista)



#=======================================================================================================
#Modelos para Entrenadores

class Entrenador(models.Model):
    estado = (
        ('Activo',True),
        ('Inactivo',False),
    )

    tipo_sexo = (
        ('Masculino','Masculino'),
        ('Femenino','Femenino'),
    )

    TIPO_IDENTIDAD = (
        ('CED', 'Cédula de ciudadanía'),
        ('CEDEX', 'Cédula de extranjero'),
        ('NIT', 'NIT'),
    )
    estado = models.BooleanField(choices=estado, default=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    sexo = models.CharField(choices=tipo_sexo,max_length=11)
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