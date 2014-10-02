Tutorial de Python en Español
=============================

Esta traducción cubre la versión 3.4.2rc1 del tutorial de Python.

La revisión que usó para hacer la traducción es esta:

* https://hg.python.org/cpython/rev/8711a0951384

utilizando la carpeta Doc/tutorial y el archivo descargado fue este:

* https://hg.python.org/cpython/archive/8711a0951384.tar.bz2

La versión OnLine de esta documentación se puede encontrar en:

* http://tutorial.python.org.ar/

Instalar los paquetes necesarios para generar el HTML / PDF
-----------------------------------------------------------

Hay un script (`dev/install_dependencies.sh`) que instala las
dependencias necesarias para generar el tutorial en todos sus
formatos.

*Abrir el archivo ANTES de ejecutarlo para estar SEGUROS que hace lo
 que queremos en vez de algo extraño*

Actualizar el tutorial
----------------------

1. Fijarse en http://hg.python.org/cpython/tags cuál es la última
versión publicada

1. Hacer click en la versión a la que estamos interesados actualizar

1. Descargar el `.bz2` desde la barra del lateral izquierdo

1. Abrir el `.bz2` y descomprimir los archivos de la carpeta
`Doc/tutorial/*.rst` en nuestro respositorio bajo el directorio
`original/`

1. Ver las diferencias entre la versión traducida y la nueva haciendo
`git diff`

1. Traducir únicamente lo que ha cambiado entre versión y versión,
haciendo los cambios en los archivos dentro del directorio `traducidos/`

1. Crear las versiones HTML y PDF (para crear esta version es
necesario tener instalado `pdftk` 2.01):

```
fab create_html
fab create_pdf
```

1. Verificar que el PDF se abre correctamente con Evince y Firefox
(preview)

1. Si tenés permisos de `admin` en el servidor, ejecutar:

```
fab deploy_all
```

1. Una vez actualizada la traducción, enviar un mail a la lista de
correo de Python Argentina para informar sobre esta actualización.
