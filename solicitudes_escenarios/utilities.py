import zipfile,tempfile
from coldeportes.settings import MEDIA_ROOT
from django.core.servers.basehttp import FileWrapper

def comprimir_archivos(query):
    """
    Marzo 6, 2016
    Autor: Daniel Correa

    Permite comprimir los adjuntos de solicitudes de escenarios ingresados por parametro en un .zip creado en memoria

    """
    temp = tempfile.TemporaryFile()
    zip_file = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    for f in query:
        zip_file.write(MEDIA_ROOT+'/adjuntos_adecuacion_escenarios/'+f.nombre_archivo(),f.nombre_archivo())

    zip_file.close()
    wrapper = FileWrapper(temp)
    return wrapper,temp