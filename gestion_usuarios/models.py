from django.db import models

PERMISOS_DIGITADOR = [
    ['add_cajacompensacion', 'cajas'],
    ['change_cajacompensacion', 'cajas'],
    ['view_cajacompensacion', 'cajas'],

    ['add_dirigente', 'dirigentes'],
    ['change_dirigente', 'dirigentes'],
    ['view_dirigente', 'dirigentes'],

    ['add_deportista', 'deportistas'],
    ['change_deportista', 'deportistas'],
    ['view_deportista', 'deportistas'],

    ['add_centroacondicionamiento', 'centros'],
    ['change_centroacondicionamiento', 'centros'],
    ['view_centroacondicionamiento', 'centros'],

    ['add_personalapoyo', 'personal_apoyo'],
    ['change_personalapoyo', 'personal_apoyo'],
    ['view_personalapoyo', 'personal_apoyo'],

    ['add_escenario', 'escenarios'],
    ['change_escenario', 'escenarios'],
    ['view_escenario', 'escenarios'],

    ['add_seleccion', 'selecciones'],
    ['change_seleccion', 'selecciones'],
    ['view_seleccion', 'selecciones'],

    ['add_centrobiomedico', 'centros_biomedicos'],
    ['change_centrobiomedico', 'centros_biomedicos'],
    ['view_centrobiomedico', 'centros_biomedicos'],

    ['add_norma', 'normas'],
    ['change_norma', 'normas'],
    ['view_norma', 'normas'],

    ['add_noticia', 'noticias'],
    ['change_noticia', 'noticias'],
    ['delete_noticia', 'noticias'],
    ['view_noticia', 'noticias'],


    ['add_evento', 'eventos'],
    ['change_evento', 'eventos'],
    ['view_evento', 'eventos'],

    ['add_escueladeportiva', 'escuelas_deportivas'],
    ['change_escueladeportiva', 'escuelas_deportivas'],
    ['view_escueladeportiva', 'escuelas_deportivas'],

    ['add_clasificado', 'publicidad'],
    ['change_clasificado', 'publicidad'],
    ['view_clasificado', 'publicidad'],

    ['add_casodoping', 'listados_doping'],
    ['change_casodoping', 'listados_doping'],
    ['view_casodoping', 'listados_doping'],

    ['add_solicitudescenario', 'solicitud'],
    ['change_solicitudescenario', 'solicitud'],
    ['view_solicitudescenario', 'solicitud'],

    ['add_listasolicitudes', 'respuesta'],
    ['change_listasolicitudes', 'respuesta'],
    ['view_listasolicitudes', 'respuesta'],

    ['add_reconocimientodeportivo', 'reconocimiento_solicitud'],
    ['change_reconocimientodeportivo', 'reconocimiento_solicitud'],
    ['view_reconocimientodeportivo', 'reconocimiento_solicitud'],

    ['add_listasolicitudesreconocimiento', 'reconocimiento_respuesta'],
    ['change_listasolicitudesreconocimiento', 'reconocimiento_respuesta'],
    ['view_listasolicitudesreconocimiento', 'reconocimiento_respuesta'],
]

PERMISOS_LECTURA = [
    ['view_cajacompensacion', 'cajas'],
    ['view_dirigente', 'dirigentes'],
    ['view_deportista', 'deportistas'],
    ['view_centroacondicionamiento', 'centros'],
    ['view_personalapoyo', 'personal_apoyo'],
    ['view_escenario', 'escenarios'],
    ['view_seleccion', 'selecciones'],
    ['view_centrobiomedico', 'centros_biomedicos'],
    ['view_norma', 'normas'],
    ['view_noticia', 'noticias'],
    ['view_escueladeportiva', 'escuelas_deportivas'],
    ['view_clasificado', 'publicidad'],
    ['view_casodoping', 'listados_doping'],
    ['view_solicitudescenario', 'solicitud'],
    ['view_listasolicitudes', 'respuesta'],
    ['view_reconocimientodeportivo', 'reconocimiento_solicitud'],
    ['view_listasolicitudesreconocimiento', 'reconocimiento_respuesta'],
    ['view_evento', 'eventos'],
]