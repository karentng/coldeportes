#encoding:utf-8

from entidades.models import *
from django.db import models


class Deportista(models.Model):
    #Datos personales
        #Identificacion
    tipo_sexo = (
        ('Hombre','Hombre'),
        ('Mujer','Mujer'),
        ('LGTBI', 'LGTBI'),
    )
    TIPO_IDENTIDAD = (
        ('TI', 'Tarjeta de Identidad'),
        ('CC', 'Cédula de ciudadanía'),
        ('CCEX', 'Cédula de extranjero'),
        ('PASS', 'Pasaporte'),
    )
    ESTADOS = (
        (0,'ACTIVO'),
        (1,'INACTIVO'),
        (2,'EN TRANSFERENCIA'),
        (3,'TRANSFERIDO'),
    )

    ETNIAS = (
        ('MESTIZO','MESTIZO'),
        ('AFROCOLOMBIANO','AFROCOLOMBIANO'),
        ('BLANCOS','BLANCOS'),
        ('COLOMBOINDIGENA','COLOMBOINDIGENA'),
        ('GITANO','GITANO'),
    )

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    genero = models.CharField(choices=tipo_sexo,max_length=11, verbose_name='Genero del Deportista',default='Hombre')
    tipo_id = models.CharField(max_length=10, choices=TIPO_IDENTIDAD, default='CC',verbose_name='Tipo de Identificación')
    identificacion = models.CharField(max_length=100,unique=True)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.ManyToManyField(Nacionalidad)
    ciudad_residencia = models.ForeignKey(Ciudad, verbose_name='Ciudad en donde esta residiendo')
    barrio = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    telefono = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
        #Entidad
    entidad = models.ForeignKey(Entidad)
        #Disciplina
    disciplinas = models.ManyToManyField(TipoDisciplinaDeportiva)    #activo = models.BooleanField()
    estado = models.IntegerField(choices=ESTADOS, default=0, verbose_name="estado del Deportista")
    video = models.URLField(max_length=1024, verbose_name='Video', null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_deportistas', null=True, blank=True)
    etnia = models.CharField(max_length=20, choices=ETNIAS,blank=True)

    def __str__(self):
        return self.nombres+" "+self.apellidos

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
    tallas_choices = (
        ('XS','XS'),
        ('S','S'),
        ('M','M'),
        ('L','L'),
        ('XL','XL'),
        ('XXL','XXL'),
    )
    deportista = models.ForeignKey(Deportista)
    peso = models.FloatField(help_text="En kg", verbose_name="Peso (kg)")
    estatura = models.IntegerField(help_text="En cm", verbose_name="Estatura (cm)")
    RH = models.CharField(max_length=4,choices=tipos_rh,default='O+')
    tipo_talla = models.CharField(max_length=7,choices=tipos_talla_choices,default='Adulto',verbose_name='Talla para')
    talla_camisa = models.CharField(max_length=3, choices=tallas_choices)
    talla_pantaloneta = models.CharField(max_length=3, choices=tallas_choices)
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

