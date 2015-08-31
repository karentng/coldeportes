#encoding:utf-8

from entidades.models import *
from django.db import models
from coldeportes.utilities import calculate_age
from django.db.models.fields.files import ImageFieldFile, FileField
from coldeportes.settings import STATIC_URL

class Deportista(models.Model):
    #Datos personales
        #Identificacion
    tipo_sexo = (
        ('Hombre','Hombre'),
        ('Mujer','Mujer'),
        ('Indefinido', 'Indefinido'),
    )
    TIPO_IDENTIDAD = (
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
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
        ('BLANCO','BLANCO'),
        ('COLOMBOINDIGENA','COLOMBOINDIGENA'),
        ('GITANO','GITANO'),
        ('PALENQUERO','PALENQUERO'),
        ('RAIZAL','RAIZAL'),
    )

    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100,verbose_name='Apellidos')
    genero = models.CharField(choices=tipo_sexo,max_length=11, verbose_name='Genero del Deportista',default='Hombre')
    tipo_id = models.CharField(max_length=10, choices=TIPO_IDENTIDAD, default='CC',verbose_name='Tipo de Identificación')
    identificacion = models.CharField(max_length=100,unique=True,verbose_name='Identificación')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    ciudad_residencia = models.ForeignKey(Ciudad, verbose_name='Ciudad en donde esta residiendo')
    barrio = models.CharField(max_length=100,verbose_name='Barrio')
    comuna = models.CharField(max_length=100,verbose_name='Comuna')
    email = models.EmailField(null=True,blank=True)
    telefono = models.CharField(max_length=100,verbose_name='Teléfono')
    direccion = models.CharField(max_length=100,verbose_name='Dirección')
    entidad = models.ForeignKey(Entidad)

    estado = models.IntegerField(choices=ESTADOS, default=0, verbose_name="estado del Deportista")
    etnia = models.CharField(max_length=20, choices=ETNIAS,blank=True)

    video = models.URLField(max_length=1024, verbose_name='Video', null=True, blank=True)
    disciplinas = models.ManyToManyField(TipoDisciplinaDeportiva,verbose_name='Disciplinas Deportivas')
    nacionalidad = models.ManyToManyField(Nacionalidad,verbose_name='Nacionalidad')
    foto = models.ImageField(upload_to='fotos_deportistas', null=True, blank=True)

    def __str__(self):
        return self.identificacion + "-" + self.nombres+" "+self.apellidos

    def edad(self):
        return calculate_age(self.fecha_nacimiento)

    def disciplinas_deportivas(self):
        return ",".join(str(x) for x in self.disciplinas.all())

    def nacionalidad_str(self):
        return ",".join(x.nombre for x in self.nacionalidad.all())

    def fotos(self):
        return [self.foto]

    def save(self, *args, **kwargs):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        self.barrio = self.barrio.upper()
        self.comuna = self.comuna.upper()
        self.direccion = self.direccion.upper()
        super(Deportista, self).save(*args, **kwargs)

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
    RH = models.CharField(max_length=4,choices=tipos_rh,default='O+',verbose_name='Tipo de sangre')
    tipo_talla = models.CharField(max_length=7,choices=tipos_talla_choices,default='Adulto',verbose_name='Talla para' )
    talla_camisa = models.CharField(max_length=3, choices=tallas_choices,verbose_name='Talla Camisa')
    talla_pantaloneta = models.CharField(max_length=3, choices=tallas_choices,verbose_name='Talla Pantaloneta')
    talla_zapato = models.CharField(max_length=2,verbose_name='Talla Zapato')
    imc = models.FloatField(verbose_name='Indice de Masa Corporal (kg/m^2)')
    porcentaje_grasa = models.FloatField(verbose_name='Porcentaje de Grasa Corporal (%)')
    masa_corporal_magra = models.FloatField(verbose_name='Masa Corporal Magra (kg)')
    eps = models.ForeignKey(EPS,verbose_name='EPS')


#Hitorial deportivo
class HistorialDeportivo(models.Model):
    tipo_his_deportivo=(
        ('Campeonato Municipal','Campeonato Municipal'),
        ('Campeonato Departamental','Campeonato Departamental'),
        ('Campeonato Nacional','Campeonato Nacional'),
        ('Campeonato Internacional','Campeonato Internacional'),
    )

    ESTADOS_AVAL = (
        ('Aprobado','Aprobado'),
        ('Pendiente','Pendiente'),
    )

    nombre = models.CharField(max_length=100,verbose_name='Nombre del campeonato')
    fecha_inicial = models.DateField(verbose_name='Fecha Iniciación')
    fecha_final = models.DateField(verbose_name='Fecha Finalización ')
    pais = models.ForeignKey(Nacionalidad)
    institucion_equipo = models.CharField(max_length=100, verbose_name='Club deportivo')
    tipo = models.CharField(choices=tipo_his_deportivo,max_length=100,verbose_name='Clase de campeonato',default='Campeonato Internacional')
    puesto = models.IntegerField(verbose_name='Puesto obtenido')
    marca = models.CharField(max_length=100,blank=True,verbose_name='Marca obtenida')
    modalidad = models.CharField(max_length=100,blank=True,verbose_name='Modalidad de competencia')
    division = models.CharField(max_length=100,blank=True,verbose_name='División de competencia')
    prueba = models.CharField(max_length=100,blank=True,verbose_name='Prueba en la que participó')
    categoria = models.CharField(max_length=100,verbose_name='Categoria en la que participó')
    estado = models.CharField(choices=ESTADOS_AVAL,default='Aprobado',max_length=50)
    deportista = models.ForeignKey(Deportista)

    def __str__(self):
        return self.deportista.nombres+':'+self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.marca = self.marca.upper()
        self.modalidad = self.modalidad.upper()
        self.division = self.division.upper()
        self.prueba = self.prueba.upper()
        self.categoria = self.categoria.upper()
        self.institucion_equipo = self.institucion_equipo.upper()
        if self.tipo not in ['Campeonato Municipal','Campeonato Departamental']:
                self.estado = 'Pendiente'

        super(HistorialDeportivo, self).save(*args, **kwargs)

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
    pais = models.ForeignKey(Nacionalidad,verbose_name='País')
    institucion = models.CharField(max_length=100,verbose_name='Institución')
    nivel = models.CharField(choices=tipo_academica,max_length=20,verbose_name='Nivel')
    estado = models.CharField(choices=tipo_estado,max_length=20,verbose_name='Estado')
    profesion =  models.CharField(max_length=100,blank=True,null=True)
    grado_semestre = models.IntegerField(verbose_name='Grado, Año o Semestre', null=True, blank=True)
    fecha_finalizacion = models.IntegerField(blank=True,null=True,verbose_name='Año Finalización')
    deportista = models.ForeignKey(Deportista)

    def save(self, *args, **kwargs):
        self.institucion = self.institucion.upper()
        self.profesion = self.profesion.upper()
        super(InformacionAcademica, self).save(*args, **kwargs)

class CambioDocumentoDeportista(models.Model):
    TIPO_IDENTIDAD = (
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
    )

    deportista = models.ForeignKey(Deportista)
    tipo_documento_anterior = models.CharField(max_length=10, choices=TIPO_IDENTIDAD, default='CC',verbose_name='Tipo de Documento Acutual', help_text='Este es el tipo de documento que tiene el deportista actualmente')
    identificacion_anterior = models.CharField(max_length=100,verbose_name='Identificación Actual',help_text='Este es el numero de documento actual o valor de documento en caso diferente a CC y TI')
    tipo_documento_nuevo = models.CharField(max_length=10, choices=TIPO_IDENTIDAD, default='CC',verbose_name='Nuevo Tipo de Documento', help_text='Este es el tipo de documento que tendrá una vez de click en cambiar')
    identificacion_nuevo = models.CharField(max_length=100,verbose_name='Nueva Identificación', help_text='Este es el numero o valor de documento que tendrá una vez de click en cambiar')
