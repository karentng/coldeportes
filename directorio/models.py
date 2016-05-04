from django.db import models
from entidades.models import *
from snd.models import *


# Create your models here.
class EscenarioView(models.Model):
    class Meta:
        managed = False
        db_table = 'reportes_tenantescenarioview'
    #campos modelo escenario
    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    latitud = models.FloatField(max_length=10)
    longitud = models.FloatField(max_length=10)
    altura = models.PositiveIntegerField()
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.PositiveIntegerField()
    barrio = models.CharField(max_length=20)
    estrato = models.CharField(max_length=1)
    nombre_administrador = models.CharField(max_length=50, null=True)
    entidad = models.ForeignKey(Entidad)    
    estado = models.IntegerField()
    #campos modelo contacto
    nombre_contacto =  models.CharField(max_length=50)
    telefono_contacto = models.CharField(max_length=20)
    email_contacto = models.EmailField()
    descripcion_contacto = models.CharField(max_length=1024, null=True)
    #campos modelo horario
    horario_id = models.IntegerField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    dias = models.ForeignKey(Dias)
    descripcion_horario = models.CharField(max_length=1024)
    #campos modelo Foto
    foto = models.ImageField(upload_to='fotos_escenarios', null=True, blank=True)
    #campo para búsqueda
    contenido = models.TextField()


class EscenarioPublicView(models.Model):
    class Meta:
        managed = False
        db_table = 'entidades_publicescenarioview'
    #campos modelo escenario
    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    latitud = models.FloatField(max_length=10)
    longitud = models.FloatField(max_length=10)
    altura = models.PositiveIntegerField()
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.PositiveIntegerField()
    barrio = models.CharField(max_length=20)
    estrato = models.CharField(max_length=1)
    nombre_administrador = models.CharField(max_length=50, null=True)
    entidad = models.ForeignKey(Entidad)    
    estado = models.IntegerField()
    #campos modelo contacto
    nombre_contacto =  models.CharField(max_length=50)
    telefono_contacto = models.CharField(max_length=20)
    email_contacto = models.EmailField()
    descripcion_contacto = models.CharField(max_length=1024, null=True)
    #campos modelo horario
    horario_id = models.IntegerField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    dias = models.ForeignKey(Dias)
    descripcion_horario = models.CharField(max_length=1024)
    #campos modelo Foto
    foto = models.ImageField(upload_to='fotos_escenarios', null=True, blank=True)
    #campo para búsqueda
    contenido = models.TextField()


class CAFView(models.Model):
    class Meta:
        managed = False
        db_table = 'reportes_tenantcafview'
    #campos cafs
    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, verbose_name="dirección")
    latitud = models.FloatField(max_length=10)
    longitud = models.FloatField(max_length=10)
    telefono_contacto = models.CharField(max_length=50, verbose_name="teléfono")
    altura = models.FloatField(max_length=10)    
    email = models.EmailField()
    web = models.URLField(verbose_name="página web", blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.CharField(max_length=10)
    barrio = models.CharField(max_length=20)
    estrato = models.IntegerField()
    nombre_administrador = models.CharField(max_length=50, blank=True, null=True)
    entidad = models.ForeignKey(Entidad)
    estado = models.IntegerField()
    #campo de modelo CAfoto
    foto = models.ImageField(upload_to='ruta_fotos_cafs')
    #campo para búsqueda
    contenido = models.TextField()


class CAFPublicView(models.Model):
    class Meta:
        managed = False
        db_table = 'entidades_publiccafview'
    #campos cafs
    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, verbose_name="dirección")
    latitud = models.FloatField(max_length=10)
    longitud = models.FloatField(max_length=10)
    telefono_contacto = models.CharField(max_length=50, verbose_name="teléfono")
    altura = models.FloatField(max_length=10)    
    email = models.EmailField()
    web = models.URLField(verbose_name="página web", blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.CharField(max_length=10)
    barrio = models.CharField(max_length=20)
    estrato = models.IntegerField()
    nombre_administrador = models.CharField(max_length=50, blank=True, null=True)
    entidad = models.ForeignKey(Entidad)
    estado = models.IntegerField()
    #campo de modelo CAfoto
    foto = models.ImageField(upload_to='ruta_fotos_cafs')
    #campo para búsqueda
    contenido = models.TextField()

    
class DeportistaView(models.Model):
    class Meta:
        managed = False
        db_table = 'reportes_tenantdeportistaview'
    #campos deportista
    nombre = models.CharField(max_length=100, db_column='nombres', verbose_name='Nombres')
    apellidos = models.CharField(max_length=100,verbose_name='Apellidos')
    genero = models.CharField(max_length=11, verbose_name='Genero del Deportista',default='Hombre')
    ciudad_residencia = models.ForeignKey(Ciudad, verbose_name='Ciudad en donde esta residiendo')
    barrio = models.CharField(max_length=100,verbose_name='Barrio')
    comuna = models.CharField(max_length=100,verbose_name='Comuna')
    email = models.EmailField(null=True,blank=True)
    telefono_contacto = models.CharField(max_length=100,verbose_name='Telefono')
    direccion = models.CharField(max_length=100,verbose_name='Direccion')
    estado = models.IntegerField(default=0, verbose_name="estado del Deportista")
    etnia = models.CharField(max_length=20, blank=True)
    nacionalidad = models.ForeignKey(Nacionalidad)
    foto = models.ImageField(upload_to='fotos_deportistas', null=True, blank=True)
    entidad = models.ForeignKey(Entidad)   
    #campo para búsqueda
    contenido = models.TextField()

    
class DeportistaPublicView(models.Model):
    class Meta:
        managed = False
        db_table = 'entidades_publicdeportistaview'
    #campos deportista
    nombre = models.CharField(max_length=100, db_column='nombres', verbose_name='Nombres')
    apellidos = models.CharField(max_length=100,verbose_name='Apellidos')
    genero = models.CharField(max_length=11, verbose_name='Genero del Deportista',default='Hombre')
    ciudad_residencia = models.ForeignKey(Ciudad, verbose_name='Ciudad en donde esta residiendo')
    barrio = models.CharField(max_length=100,verbose_name='Barrio')
    comuna = models.CharField(max_length=100,verbose_name='Comuna')
    email = models.EmailField(null=True,blank=True)
    telefono_contacto = models.CharField(max_length=100,verbose_name='Telefono')
    direccion = models.CharField(max_length=100,verbose_name='Direccion')
    estado = models.IntegerField(default=0, verbose_name="estado del Deportista")
    etnia = models.CharField(max_length=20, blank=True)
    nacionalidad = models.ForeignKey(Nacionalidad)
    foto = models.ImageField(upload_to='fotos_deportistas', null=True, blank=True)
    entidad = models.ForeignKey(Entidad)   
    #campo para búsqueda
    contenido = models.TextField()
     

class PersonalApoyoView(models.Model):
    class Meta:
        managed = False
        db_table = 'reportes_tenantpersonalapoyoview'
    #campos deportista
    nombre = models.CharField(max_length=100, db_column='nombres', verbose_name='Nombres')
    telefono_contacto = models.CharField(max_length=100,verbose_name='Telefono')
    apellidos = models.CharField(max_length=100,verbose_name='Apellidos')
    genero = models.CharField(verbose_name='Género', max_length=11)
    telefono_celular = models.CharField(max_length=50, verbose_name='Teléfono celular', blank=True)
    ciudad = models.ForeignKey(Ciudad, verbose_name='Ciudad en donde esta residiendo')
    correo_electronico = models.EmailField(blank=True,verbose_name='Correo electrónico')
    nacionalidad = models.ForeignKey(Nacionalidad)
    entidad = models.ForeignKey(Entidad)
    estado = models.IntegerField(default=0)
    etnia = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='fotos_personal_apoyo', null=True, blank=True)
    #campo para búsqueda
    contenido = models.TextField()

     
class PersonalApoyoPublicView(models.Model):
    class Meta:
        managed = False
        db_table = 'entidades_publicpersonalapoyoview'
    #campos deportista
    nombre = models.CharField(max_length=100, db_column='nombres', verbose_name='Nombres')
    telefono_contacto = models.CharField(max_length=100,verbose_name='Telefono')
    apellidos = models.CharField(max_length=100,verbose_name='Apellidos')
    genero = models.CharField(verbose_name='Género', max_length=11)
    telefono_celular = models.CharField(max_length=50, verbose_name='Teléfono celular', blank=True)
    ciudad = models.ForeignKey(Ciudad, verbose_name='Ciudad en donde esta residiendo')
    correo_electronico = models.EmailField(blank=True,verbose_name='Correo electrónico')
    nacionalidad = models.ForeignKey(Nacionalidad)
    entidad = models.ForeignKey(Entidad)
    estado = models.IntegerField(default=0)
    etnia = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='fotos_personal_apoyo', null=True, blank=True)
    #campo para búsqueda
    contenido = models.TextField()


class DirigenteView(models.Model):
    class Meta:
        managed = False
        db_table = 'reportes_tenantdirigenteview'
    nombre = models.CharField(max_length=100, db_column='nombres')
    cargo = models.CharField(max_length=100, verbose_name="Nombre del cargo")
    apellidos = models.CharField(max_length=100)
    genero = models.CharField(max_length=6, verbose_name='Género')
    ciudad = models.ForeignKey(Ciudad, verbose_name="Ciudad de residencia")
    telefono_contacto = models.CharField(max_length=100, verbose_name="Teléfono")
    email = models.EmailField(null=True,blank=True)
    nacionalidad = models.ForeignKey(Nacionalidad)
    estado = models.IntegerField(default=0, verbose_name="Estado del dirigente")    
    foto = models.ImageField(null=True, blank=True)
    entidad = models.ForeignKey(Entidad) 
    #campo para búsqueda
    contenido = models.TextField()


class DirigentePublicView(models.Model):

    class Meta:
        managed = False
        db_table = 'entidades_publicdirigenteview'

    nombre = models.CharField(max_length=100, db_column='nombres')
    cargo = models.CharField(max_length=100, verbose_name="Nombre del cargo")
    apellidos = models.CharField(max_length=100)
    genero = models.CharField(max_length=6, verbose_name='Género')
    ciudad = models.ForeignKey(Ciudad, verbose_name="Ciudad de residencia")
    telefono_contacto = models.CharField(max_length=100, verbose_name="Teléfono")
    email = models.EmailField(null=True,blank=True)
    nacionalidad = models.ForeignKey(Nacionalidad)
    estado = models.IntegerField(default=0, verbose_name="Estado del dirigente")    
    foto = models.ImageField(null=True, blank=True)
    entidad = models.ForeignKey(Entidad) 
    #campo para búsqueda
    contenido = models.TextField()


class CajaCompensacionView(models.Model):
    class Meta:
        managed = False
        db_table = 'reportes_tenantcajasview'
    nombre =  models.CharField(max_length=100)    
    clasificacion = models.CharField(max_length=1)
    foto = models.ImageField(null=True, blank=True)
    entidad = models.ForeignKey(Entidad)    
    estado = models.IntegerField(default=0, verbose_name="estado del Escenario")
    nombre_contacto =  models.CharField(max_length=50)
    telefono_contacto = models.CharField(max_length=20)
    email = models.EmailField()
    ciudad = models.ForeignKey(Ciudad, verbose_name="Ciudad")    
    #campo para búsqueda
    contenido = models.TextField()


class CajaCompensacionPublicView(models.Model):

    class Meta:
        managed = False
        db_table = 'entidades_publiccajasview'

    nombre =  models.CharField(max_length=100)    
    clasificacion = models.CharField(max_length=1)
    foto = models.ImageField(null=True, blank=True)
    entidad = models.ForeignKey(Entidad)    
    estado = models.IntegerField(default=0, verbose_name="estado del Escenario")
    nombre_contacto =  models.CharField(max_length=50)
    telefono_contacto = models.CharField(max_length=20)
    email = models.EmailField()
    ciudad = models.ForeignKey(Ciudad, verbose_name="Ciudad")    
    #campo para búsqueda
    contenido = models.TextField()

