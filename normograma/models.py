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

    AÑOS = zip( range(1980,2017), range(1980,2017) )
    JURISDICCIONES = (('D', 'Departamental'), ('M', 'Municipal'), ('N', 'Nacional'))
    
    norma =  models.CharField(max_length=100,unique=True, verbose_name="título de la norma")
    palabras_clave = models.CharField(max_length=1024, verbose_name='palabras clave')
    año = models.IntegerField(default=0, choices=AÑOS, verbose_name="año")
    sector = models.CharField(max_length=150)
    jurisdiccion = models.CharField(max_length=2, choices=JURISDICCIONES, verbose_name="jurisdicción")
    archivo = models.FileField(upload_to=foto_name, verbose_name="subir archivo")
    descripcion = models.TextField(max_length=1024, verbose_name='descripción')
    contenido_busqueda = models.TextField(editable=False)

    def save(self, *args, **kwargs):
        self.contenido_busqueda = self.norma+" "+self.palabras_clave+" "+str(self.año)
        super(Norma,self).save(*args, **kwargs)