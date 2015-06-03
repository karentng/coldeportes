Instalación
========================================

Instalar los requerimientos

    pip install -r requirements.txt

Se recomienda leer la documentación acerca de django-tenant-schemas en:

	https://django-tenant-schemas.readthedocs.org/en/latest/index.html

Clonar el repositorio https://github.com/tomturner/django-tenant-schemas, copiamos la carpeta "tenant_schemas" en el directorio de paquetes de Python.

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


Manejo del Repositorio
==========================

Para subir al repositorio cada usuario esta autorizado de la siguiente manera:

Rama "milton-daniel": Miltón y Daniel pueden leer y escribir

Rama "cristian": Cristian puede leer y escribir

Rama "Andres-Karent": Andrés y Karent pueden leer y escribir

Rama "master": Mauricio Gaona puede leer y escribir

Nota: Cada persona autorizada solo puede escribir en la rama correspondiente.

Proceso para hacer PUSH
==========================
	git checkout nombre_rama (Para cambiar a la rama de trabajo)
	git add archivo1 archivo2 ... (Si son todos los archivos: git add .)
	git commit -m "Mensaje del commit"
	git push