INSERT INTO indervalle.snd_personalapoyo (id,actividad,nombres, apellidos,genero,tipo_id,identificacion,telefono_fijo,telefono_celular,
                            correo_electronico,fecha_nacimiento,ciudad_id,entidad_id,estado,etnia) VALUES
(100,1,'JUAN PEDRO','GONZALEZ MEJIA','HOMBRE','CED','11440908798','3729434','3137654326','juanpe@hotmail.com','1990-10-26',54,2,1,'MESTIZO');

INSERT INTO indervalle.snd_personalapoyo_nacionalidad (id,personalapoyo_id,nacionalidad_id) VALUES
(100,100,52);

INSERT INTO indervalle.snd_experiencialaboral (id,nombre_cargo,institucion,fecha_comienzo,actual,fecha_fin,personal_apoyo_id) VALUES
(100,'ENTRENADOR DE FUTBOL','INDERVALLE','2012-07-01',FALSE,'2015-01-01',100);

INSERT INTO indervalle.snd_formaciondeportiva (id,denominacion_diploma,nivel,institucion_formacion,fecha_comienzo,actual,fecha_fin,personal_apoyo_id,pais_formacion_id) VALUES
(100,'ENTRENADOR DE FUTBOL','AVANZADO','ESCUELA DE FUTBOL EL PIBE','2012-07-01',FALSE,'2015-01-01',100,52);

INSERT INTO indervalle.snd_formaciondeportiva_disciplina_deportiva (id,formaciondeportiva_id,tipodisciplinadeportiva_id) VALUES
(100,100,3);
