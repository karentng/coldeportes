INSERT INTO indervalle.snd_deportista (id,nombres, apellidos,genero,tipo_id,identificacion,fecha_nacimiento,barrio,comuna,email,telefono,direccion,entidad_id,estado,etnia,ciudad_residencia_id,video,foto) VALUES
(3,'ANDRES','PEREZ','Hombre','CC','11441237654','1992-07-07','MELENDEZ','12','aperez@deporcali.com','3127693402','CALLE 5 # 39 00',2,0,'''',152,'''','''');

INSERT INTO indervalle.snd_composicioncorporal (id,peso,estatura,"RH",tipo_talla,talla_camisa,talla_pantaloneta,talla_zapato,deportista_id,imc,masa_corporal_magra,porcentaje_grasa,eps_id) VALUES 
(3,72,172,'O+','Adulto','S','S','40',3,20,20,20,1);

INSERT INTO indervalle.snd_deportista_disciplinas (id,deportista_id,tipodisciplinadeportiva_id) VALUES
(3,3,4);

INSERT INTO indervalle.snd_deportista_nacionalidad (id,deportista_id,nacionalidad_id) VALUES
(3,3,52);

INSERT INTO indervalle.snd_historialdeportivo (id,fecha_inicial, institucion_equipo,tipo,deportista_id,fecha_final,actual,categoria,division,marca,modalidad,nombre,pais_id,prueba,puesto) VALUES
(3,'2015-07-27','INTER DE MILAN','Campeonato Internacional',3,NULL,TRUE,'MAYORES','''','''','FUTBOL 11','MUNDIAL DE CLUBES',112,'''',1);

INSERT INTO indervalle.snd_informacionacademica (id,institucion,nivel,estado,profesion,grado_semestre,fecha_finalizacion,deportista_id,pais_id) VALUES
(3,'UNIVALLE','Pregrado','Finalizado','INGENIERO DE SISTEMAS',NULL,2016,3,52);