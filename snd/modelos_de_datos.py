from snd.models import *

'''
(
    (
        MODELO,
        [CAMPOS A FILTRAR/DESPLEGAR],
        [CAMPOS A DESPLEGAR],
        [['COLUMNA',[[COMPARACION, ESTILO]+]]]|None,
        [
            [
                NOMBRE A DESPLEGAR,
                URL,
                [PARAMETROS DEL URL],
                IMAGEN FA,
                [
                    [
                        [(campo)+],
                        [(valorCampo)+],
                        funcionDeEvaluacion
                    ]+
                ] | None
            ]+ | []
        ],
        False | True            -> Se consulta en todos los tenants o no
    ),
)
'''

MODELOS_DE_DATOS = (
    (
        CentroAcondicionamiento,
        ['nombre','direccion', 'telefono', 'ciudad', 'email', 'web', 'estado'],
        ['Nombre','Dirección', 'Teléfono', 'Ciudad', 'Email', 'Página Web', 'Estado'],
        None,
        [
            [
                "Ver CAF",
                'ver_caf',
                ['id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'crear_caf',
                ['Identificación', 'id'],
                'fa-gear',
                None
            ],
        ],
    ),
    (
        Deportista,
        ["nombres apellidos","ciudad_residencia","tipo_id","identificacion","edad","disciplinas_deportivas","estado"],
        ["Nombre","Ciudad de residencia","Tipo Identificación","Identificación","Edad","Disciplinas","Estado"],
        None,
        [
            [
                "Ver Deportista" ,
                'ver_deportista',
                ['id'],
                'fa-eye',
                None
            ],
        ]
    ),
)

'''
    [
        "Activar/Desactivar",
        'desactivar_caf',
        ['id'],
        'fa-ban',
        None
    ],
'''