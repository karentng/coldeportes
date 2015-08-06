INSERT INTO indervalle.snd_entrenador (id,nombres, apellidos,genero,tipo_id,nro_id,telefono_fijo,telefono_celular,
                            correo_electronico,fecha_nacimiento,altura,peso,ciudad_id,entidad_vinculacion_id,estado) VALUES
(100,'JUAN PEDRO','GONZALEZ MEJIA','HOMBRE','CED','11440908798','3729434','3137654326','juanpe@hotmail.com','1990-10-26','156','70',54,2,1);

INSERT INTO indervalle.snd_entrenador_nacionalidad (id,entrenador_id,nacionalidad_id) VALUES
(100,100,52);

INSERT INTO indervalle.snd_experiencialaboral (id,nombre_cargo,institucion,fecha_comienzo,actual,fecha_fin,entrenador_id) VALUES
(100,'ENTRENADOR DE FUTBOL','INDERVALLE','2012-07-01',FALSE,'2015-01-01',100);

INSERT INTO indervalle.snd_formaciondeportiva (id,denominacion_diploma,nivel,institucion_formacion,fecha_comienzo,actual,fecha_fin,entrenador_id,pais_formacion_id) VALUES
(100,'ENTRENADOR DE FUTBOL','AVANZADO','ESCUELA DE FUTBOL EL PIBE','2012-07-01',FALSE,'2015-01-01',100,52);

INSERT INTO indervalle.snd_formaciondeportiva_disciplina_deportiva (id,formaciondeportiva_id,tipodisciplinadeportiva_id) VALUES
(100,100,3);
