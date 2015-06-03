Instalación
===========

Instalar los requerimientos

    pip install -r requirements.txt

Se recomienda leer la documentación acerca de django-tenant-schemas en:

	https://django-tenant-schemas.readthedocs.org/en/latest/index.html

Realizar los pasos para el fix de django-tenant-schemas en Django 1.8:

	Parte 1: https://github.com/tomturner/django-tenant-schemas/commit/fe437f7c81af8484614b3dcdaeb7ad5c43249f54
	Parte 2: https://github.com/tomturner/django-tenant-schemas/commit/d56c2538162abe1603b13290d2c5f40825c22711

Sincronice la base de datos:
	
	python manage.py makemigrations
	python manage.py migrate_schemas (no se usara migrate, siempre migrate_schemas)

Dentro de la base de datos, ir al esquema "public", en él registrar dentro de la tabla "entidades_entidad" la entidad:
	
	domain_url = localhost (para pruebas locales -- cambiar si se configura en otro host que apunte al localhost --)
	schema_name = public
	nombre = public

	Nota: Sin este paso, la aplicación no funcionará correctamente, debido a que necesita el tenant público

Ejecutar el servidor:

	python manage.py runserver