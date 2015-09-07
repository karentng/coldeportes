#encoding:utf-8
from django.db import models
from django.db import models

def foto_name(instance, filename):
        #el nombre de la imagen es el id de la norma junto con el año de la misma
        #primero se borra alguna imagen existente que tenga el mismo nombre. Si la imagen anterior tiene una extensión distinta a la nueva se crea una copia
        ruta = 'normas/' + instance.id +"_"+ instance.año 
        ruta_delete = settings.MEDIA_ROOT + "/" + ruta
        if(os.path.exists(ruta_delete)):
            os.remove(ruta_delete)
        return ruta

class Norma(models.Model):
    sectores = (
        ('D', 'Deporte'),
        ('E', 'Educación Física'),
        ('R', 'Recreación'),
    )
    norma =  models.CharField(max_length=100,unique=True)
    sector = models.CharField(choices=sectores, max_length=1)
    año = models.IntegerField(default=0, verbose_name="año")
    descripcion = models.TextField(max_length=1024, verbose_name='descripción', null=True)
    palabras_clave = models.TextField(max_length=1024, verbose_name='palabras clave')
    foto = models.FileField(upload_to=foto_name, null=True, blank=True)
