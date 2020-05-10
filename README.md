Tutorial de Python en Español
=============================


:warning: **Este repo contiene la versión original de la traducción del tutorial. Recientemente la migramos al formato oficial para poder tenerlo disponible en docs.python.org**

El repositorio con el formato oficial es: https://github.com/PyCampES/python-docs-es 

Esta traducción cubre la versión 3.6.3 del tutorial de Python.

Utilizando la carpeta Doc/tutorial y el archivo descargado fue este:

* https://github.com/python/cpython/tree/v3.6.3/Doc/tutorial

La versión OnLine de esta documentación se puede encontrar en:

* https://tutorial.python.org.ar/


Hosteado en Read The Docs: [![Documentation Status](https://readthedocs.org/projects/python-tutorial-es/badge/?version=latest)](https://tutorial.python.org.ar/en/latest/?badge=latest)

Actualizar el tutorial
----------------------

1. Fijarse en https://github.com/python/cpython/releases cuál es la última
versión publicada

1. Descargar el `.tar.gz` que aparece al lado del nombre de la versión

1. Abrir el `.tar.gz` y descomprimir los archivos de la carpeta
`Doc/tutorial/*.rst` en nuestro respositorio bajo el directorio
`original/`

1. Ver las diferencias entre la versión traducida y la nueva haciendo
`git diff`

1. Traducir únicamente lo que ha cambiado entre versión y versión,
haciendo los cambios en los archivos dentro del directorio
`traducidos/`

1. Actualizar las variales `version` y `release` del archivo
   `traducidos/conf.py`.

1. Actualizar la fecha en el archivo `traducidos/imagenes/pag1.svg`

1. Crear las versiones HTML, eBook y PDF (para crear esta version es
necesario tener instalado `pdftk` 2.01):

1. Actualizar el README.md (la sección que indica qué versión del
   tutorial está traducida, al principio)

1. Crear un commit para esta nueva revision:
   ```
   git commit -am "Actualización del tutorial"
    ```

1. Crear una etiqueta de git:
   ```
   git tag v3.6.3
   git push --tags
   ```

1. Una vez actualizada la traducción. Cuando el PR es aceptado y "mergeado" a master la documentación se va a actualizar 
   automaticamente en Read the Docs

