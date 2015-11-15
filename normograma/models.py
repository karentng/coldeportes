#encoding:utf-8
from django.db import models
from django.conf import settings
from entidades.models import Ciudad
import os


class TipoSector(models.Model):

    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre


def foto_name(instance, filename):
    #el nombre de la imagen es el id de la norma junto con el año de la misma
    #primero se borra alguna imagen existente que tenga el mismo nombre. Si la imagen anterior tiene una extensión distinta a la nueva se crea una copia
    ruta = 'normas/' + instance.norma +"_"+ str(instance.anio) + filename[-4:]
    ruta_delete = settings.MEDIA_ROOT + "/" + ruta
    if(os.path.exists(ruta_delete)):
        os.remove(ruta_delete)
    return ruta


class Norma(models.Model):

    JURISDICCIONES = (('D', 'Departamental'), ('M', 'Municipal'), ('N', 'Nacional'))
    ANIOS = zip( range(1980,2017), range(1980,2017) )
    
    norma =  models.CharField(max_length=100,unique=True, verbose_name="título de la norma")
    palabras_clave = models.CharField(max_length=1024, verbose_name='palabras clave')
    anio = models.IntegerField(default=2015, verbose_name="año", choices=ANIOS)
    sectores = models.ManyToManyField(TipoSector)
    jurisdiccion = models.CharField(max_length=2,verbose_name="jurisdicción", choices=JURISDICCIONES)
    ciudad = models.ForeignKey(Ciudad, verbose_name="ciudad de donde se hace el registro")
    archivo = models.FileField(upload_to=foto_name, verbose_name="subir archivo", null=True, blank=True)
    descripcion = models.TextField(max_length=1024, verbose_name='descripción')
    contenido_busqueda = models.TextField(editable=False)

    class Meta:
        permissions = (
            ("view_norma", "Permite ver norma"),
        )

    def save(self, *args, **kwargs):
        self.contenido_busqueda = self.norma+" "+self.palabras_clave+" "+str(self.anio)
        super(Norma,self).save(*args, **kwargs)


    def obtenerAtributos(self):
        atributos = [
            ["Título", self.norma],
            ["Año", self.anio],
            ["Jurisdicción", self.jurisdiccion],
            ["Archivo", self.archivo],
        ]

        return [self.norma, atributos, None, None, "Normas!"]

