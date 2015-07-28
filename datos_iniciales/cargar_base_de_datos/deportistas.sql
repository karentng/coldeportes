INSERT INTO entidad1.snd_deportista (id,nombres, apellidos,genero,tipo_id,identificacion,fecha_nacimiento,barrio,comuna,email,telefono,direccion,activo,video,foto,ciudad_nacimiento_id,entidad_id) VALUES
(2,'ANDRES FELIPE','ROA','Hombre','CC','11448808798','1990-10-26','CANEY','12','aroaaa@deporcali.com','3129807898','CALLE 56 # 45 09',TRUE,'''','''',5,3);

INSERT INTO entidad1.snd_composicioncorporal (id,peso,estatura,"RH",tipo_talla,talla_camisa,talla_pantaloneta,talla_zapato,porcentaje_grasa,porcentaje_musculo,deportista_id) VALUES 
(2,81,180,'O+','Adulto','M','M','41','12','80',2);

INSERT INTO entidad1.snd_deportista_disciplinas (id,deportista_id,tipodisciplinadeportiva_id) VALUES
(2,2,4);

INSERT INTO entidad1.snd_deportista_nacionalidad (id,deportista_id,nacionalidad_id) VALUES
(2,2,52);

INSERT INTO entidad1.snd_historialdeportivo (id,fecha ,lugar ,descripcion ,institucion_equipo ,tipo ,deportista_id) VALUES
(2,'2015-06-01','COLOMBIA','CAMPEÓN LIGA AGUILA II','DEPORTIVO CALI','Competencia',2);

INSERT INTO entidad1.snd_informacionacademica (id,institucion,nivel,estado,profesion,grado_semestre,deportista_id,pais_id) VALUES
(2,'UNIVALLE','Pregrado','Actual','DEPORTE',2,2,52);