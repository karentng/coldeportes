from django.db import connection

def checkear_inicializacion_directorio():
    """try:
        EscenarioView.objects.all().exists()
        CAFView.objects.all().exists()
        DeportistaView.objects.all().exists()
        PersonalApoyoView.objects.all().exists()
        DirigenteView.objects.all().exists()
        CajaCompensacionView.objects.all().exists()

    except Exception:"""
    #crear_vistas()

def crear_vistas():
    sql = """create or replace view directorio_escenarioview as 
    select  E.id, E.nombre,
            E.direccion, E.latitud,         
            E.longitud, E.altura,       
            E.ciudad_id, E.comuna,      
            E.barrio, E.estrato,        
            E.nombre_administrador,         
            E.entidad_id, E.estado,         
            C.nombre as nombre_contacto,        
            C.telefono as telefono_contacto,        
            C.email as email_contacto,      
            C.descripcion as descripcion_contacto,
            H.id as horario_id,      
            H.hora_inicio,      
            H.hora_fin,     
            HD.dias_id,     
            H.descripcion as descripcion_horario,       
            F.foto,     
            E.nombre||' '||EN.nombre as contenido
    from snd_escenario E 
    LEFT join snd_contacto C on C.escenario_id=E.id 
    LEFT join snd_horariodisponibilidad H on H.escenario_id=E.id
    LEFT join snd_horariodisponibilidad_dias HD on HD.horariodisponibilidad_id=H.id
    LEFT join snd_foto F on F.escenario_id=E.id 
    LEFT join public.entidades_entidad EN on E.entidad_id=EN.id;

    create or replace view directorio_cafview as 
    select  CAF.id, CAF.nombre,
            CAF.direccion, CAF.latitud,         
            CAF.longitud, CAF.telefono as telefono_contacto,
            CAF.altura, CAF.email,
            CAF.web, CAF.ciudad_id, CAF.comuna,      
            CAF.barrio, CAF.estrato,        
            CAF.nombre_administrador,         
            CAF.entidad_id, CAF.estado,
            CF.foto,     
            CAF.nombre||' '||EN.nombre as contenido
    from snd_centroacondicionamiento CAF
    LEFT join snd_cafoto CF on CF.centro_id=CAF.id 
    LEFT join public.entidades_entidad EN on CAF.entidad_id=EN.id;

    create or replace view directorio_deportistaview as 
    select  D.id, D.nombres,
            D.apellidos, D.genero,         
            D.direccion, D.telefono as telefono_contacto,
            D.ciudad_residencia_id,
            D.email,  
            D.comuna, D.barrio,
            DPN.nacionalidad_id,         
            D.entidad_id, D.estado, D.etnia,        
            D.foto,     
            D.nombres||' '||D.apellidos as contenido
    from snd_deportista D
    LEFT join snd_deportista_nacionalidad DPN on DPN.deportista_id=D.id
    LEFT join public.entidades_nacionalidad N on DPN.nacionalidad_id=N.id
    LEFT join public.entidades_entidad EN on D.entidad_id=EN.id;

    create or replace view directorio_personalapoyoview as
    select  EN.id, EN.nombres,
            EN.telefono_fijo as telefono_contacto,
            EN.apellidos, EN.genero,         
            EN.telefono_celular,
            EN.ciudad_id,
            EN.correo_electronico,      
            ENN.nacionalidad_id,         
            EN.entidad_id, EN.estado, EN.etnia,
            EN.foto,     
            EN.nombres||' '||EN.apellidos||' '||E.nombre as contenido
    from snd_personalapoyo EN
    LEFT join public.entidades_entidad E on EN.entidad_id=E.id
    LEFT join snd_personalapoyo_nacionalidad ENN on ENN.personalapoyo_id=EN.id
    LEFT join public.entidades_nacionalidad N on ENN.nacionalidad_id=N.id;

    DROP VIEW IF EXISTS directorio_dirigenteview;
    create or replace view directorio_dirigenteview as 
    select  DI.id, DI.nombres,
            DI.apellidos, DI.genero,
            DI.ciudad_residencia_id,
            DI.email, DI.telefono_fijo as telefono_contacto, 
            DIN.nacionalidad_id,         
            DI.entidad_id, DI.estado,       
            DI.foto,     
            DI.nombres||' '||DI.apellidos||' '||EN.nombre as contenido,            
            C.cargo
    from snd_dirigente DI
    LEFT join public.entidades_entidad EN on DI.entidad_id=EN.id
    LEFT join snd_dirigente_nacionalidad DIN on DIN.dirigente_id=DI.id
    LEFT join public.entidades_nacionalidad N on DIN.nacionalidad_id=N.id
    LEFT join (SELECT DIC.id, DIC.dirigente_id, DIC.nombre as cargo, max(fecha_posesion) as fecha_posesion_cargo FROM snd_dirigentecargo as DIC group by DIC.id) C on C.dirigente_id=DI.id;

    create or replace view directorio_cajacompensacionview as 
    select  CC.id, CC.nombre,
            CC.estado, CC.entidad_id,
            CC.ciudad_id,
            CC.clasificacion,
            CC.foto,
            CC.telefono_contacto, CC.email,
            CC.nombre_contacto,
            CC.nombre||' '||EN.nombre as contenido
    from snd_cajacompensacion CC
    LEFT join public.entidades_entidad EN on CC.entidad_id=EN.id;"""

    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql)
    r=connection.commit()
    return r