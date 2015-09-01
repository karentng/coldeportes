import operator
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
                ['id','entidad.id'],
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
    #MODELO DE DATOS CAF PARA LIGAS Y FEDERACIONES
    (
        CentroAcondicionamiento,
        ['nombre','direccion', 'telefono', 'ciudad', 'email', 'web', 'entidad'],
        ['Nombre','Dirección', 'Teléfono', 'Ciudad', 'Email', 'Página Web', 'Entidad'],
        None,
        [
            [
                "Ver CAF",
                'ver_caf',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
        ],
    ),
    (
        Deportista,
        ["foto","nombres apellidos","ciudad_residencia","tipo_id","identificacion","edad","disciplinas_deportivas","estado"],
        ["Foto","Nombre","Ciudad de residencia","Tipo Identificación","Identificación","Edad","Disciplinas","Estado"],
        None,
        [
            [
                "Ver Deportista",
                'ver_deportista',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'edicion_deportista',
                ['id'],
                'fa-gear',
                [
                    [
                        ['estado'],
                        ['ACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0])
                    ]
                ]

            ],
            [
                "CTD",
                'cambio_documento_deportista',
                ['id'],
                'fa-archive',
                [
                    [
                        ['estado'],
                        ['ACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0])
                    ]
                ]

            ],
            [
                "A/I",
                'deportista_desactivar',
                ['id'],
                'fa-ban',
                [
                    [
                        ['estado'],
                        ['ACTIVO','INACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0]) or operator.eq(x[0], y[1])
                    ]
                ]

            ],
            [
                "Transferir",
                'generar_transferencia',
                ['1','1','id'],
                'fa-exchange',
                [
                    [
                        ['estado'],
                        ['ACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0])
                    ]
                ]

            ],
            [
                "Cancelar Transferencia",
                'cancelar_transferencia',
                ['id','1'],
                'fa-times',
                [
                    [
                        ['estado'],
                        ['EN TRANSFERENCIA'],
                        lambda x, y: operator.eq(x[0], y[0])
                    ]
                ]

            ],

        ],
    ),
    #MODELO DE DATOS PARA DEPORTISTAS PARA EL TENANT TIPO LIGA Y FEDERACIÓN
    (
        Deportista,
        ["foto","nombres apellidos","ciudad_residencia","tipo_id","identificacion","edad","disciplinas_deportivas","entidad"],
        ["Foto","Nombre","Ciudad de residencia","Tipo Identificación","Identificación","Edad","Disciplinas","Entidad"],
        None,
        [
            [
                "Ver Deportista",
                'ver_deportista',
                ['id','entidad.id'],
                'fa-eye',
                None
            ]
        ],
    ),
    (
        PersonalApoyo,
        ['foto','nombres apellidos', 'actividad', 'identificacion', 'estado'],
        ['foto','Nombre', 'Actividad desempeñada', 'Identificación', 'Estado'],
        None,
        [
            [
                "Ver más",
                'ver_personal_apoyo',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'edicion_personal_apoyo',
                ['id'],
                'fa-gear',
                None
            ],
            [
                "A/I",
                'personal_apoyo_desactivar',
                ['id'],
                'fa-ban',
                [
                    [
                        ['estado'],
                        ['ACTIVO','INACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0]) or operator.eq(x[0], y[1])
                    ]
                ]

            ],
            [
                "Transferir",
                'generar_transferencia',
                ['1','2','id'],
                'fa-exchange',
                [
                    [
                        ['estado'],
                        ['ACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0])
                    ]
                ]

            ],
            [
                "Cancelar Transferencia",
                'cancelar_transferencia',
                ['id','2'],
                'fa-times',
                [
                    [
                        ['estado'],
                        ['EN TRANSFERENCIA'],
                        lambda x, y: operator.eq(x[0], y[0])
                    ]
                ]

            ],
        ],
    ),
    #MODELO DE DATOS PARA PERSONAL DE APOYO PARA FEDERACIONES Y CLUBES
    (
        PersonalApoyo,
        ['foto','nombres apellidos', 'actividad', 'identificacion', 'entidad'],
        ['Foto','Nombre', 'Actividad desempeñada', 'Identificación', 'Entidad'],
        None,
        [
            [
                "Ver más",
                'ver_personal_apoyo',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'edicion_personal_apoyo',
                ['id'],
                'fa-gear',
                None
            ],
            [
                "A/I",
                'personal_apoyo_desactivar',
                ['id'],
                'fa-ban',
                [
                    [
                        ['estado'],
                        ['ACTIVO','INACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0]) or operator.eq(x[0], y[1])
                    ]
                ]

            ]
        ],
    ),
    (
        Dirigente,
        ['foto','identificacion','nombres apellidos', 'estado'],
        ['Foto','Identificación','Nombre', 'Estado'],
        None,
        [
            [
                "Ver más",
                'dirigentes_ver',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'dirigentes_wizard_identificacion',
                ['id'],
                'fa-gear',
                None
            ],
            [
                "A/I",
                'dirigentes_activar_desactivar',
                ['id'],
                'fa-ban',
                [
                    [
                        ['estado'],
                        ['ACTIVO','INACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0]) or operator.eq(x[0], y[1])
                    ]
                ]

            ]
        ],
    ),
    #MODELO DE DATOS DIRIGENTE PARA LIGA Y FEDERACIÓN
    (
        Dirigente,
        ['foto','identificacion','nombres apellidos', 'entidad'],
        ['Foto','Identificación','Nombre', 'Entidad'],
        None,
        [
            [
                "Ver más",
                'dirigentes_ver',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'dirigentes_wizard_identificacion',
                ['id'],
                'fa-gear',
                None
            ],
            [
                "A/I",
                'dirigentes_activar_desactivar',
                ['id'],
                'fa-ban',
                [
                    [
                        ['estado'],
                        ['ACTIVO','INACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0]) or operator.eq(x[0], y[1])
                    ]
                ]

            ]
        ],
    ),
    (
        Escenario,
        ['nombre','ciudad','estrato', 'estado'],
        ['Nombre','Ciudad(Departamento)','Estrato', 'Estado'],
        None,
        [
            [
                "Ver más",
                'ver_escenario',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'wizard_identificacion',
                ['id'],
                'fa-gear',
                None
            ],
            [
                "A/I",
                'desactivar_escenario',
                ['id'],
                'fa-ban',
                [
                    [
                        ['estado'],
                        ['ACTIVO','INACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0]) or operator.eq(x[0], y[1])
                    ]
                ]

            ]
        ],
    ),
    #MODELO DE DATOS PARA ESCENARIO LIGAS Y FEDERACIONES
    (
        Escenario,
        ['nombre','ciudad','estrato', 'entidad'],
        ['Nombre','Ciudad(Departamento)','Estrato', 'Entidad'],
        None,
        [
            [
                "Ver más",
                'ver_escenario',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
        ],
    ),
    (
        Seleccion,
        ["nombre", "tipo", "fecha_inicial", "fecha_final", "campeonato", "tipo_campeonato"],
        ["Nombre", "Tipo de Selección", "Fecha Convocatoria", "Fecha Finaliza Convocatoria", "Nombre Campeonato", "Tipo Campeonato"],
        None,
        [
            [
                "Ver Seleccion",
                'ver_seleccion',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'editar_seleccion',
                ['id'],
                'fa-gear',
                None
            ],
        ],
    ),
)
