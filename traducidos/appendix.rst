.. _tut-appendix:

********
Apéndice
********


.. _tut-interac:

Modo interactivo
================

.. _tut-error:

Manejo de errores
-----------------

Cuando ocurre un error, el intérprete imprime un mensaje de error y la traza
del error.  En el modo interactivo, luego retorna al prompt primario; cuando la
entrada viene de un archivo, el programa termina con código de salida distinto
a cero luego de imprimir la traza del error. (Las excepciones manejadas por una
clausula :keyword:`except` en una sentencia :keyword:`try` no son errores en
este contexto).  Algunos errores son incondicionalmente fatales y causan una
terminación con código de salida distinto de cero; esto se debe a
inconsistencias internas o a que el intérprete se queda sin memoria.
Todos los mensajes de error se escriben en el flujo de errores estándar;
las salidas normales de comandos ejecutados se escriben en la salida estándar.

Al ingresar el caracter de interrupción (por lo general Control-C o DEL) en el
prompt primario o secundario, se cancela la entrada y retorna al prompt
primario.  [#]_ Tipear una interrupción mientras un comando se están ejecutando
lanza la excepción :exc:`KeyboardInterrupt`, que puede ser manejada con una
sentencia :keyword:`try`.


.. _tut-scripts:

Programas ejecutables de Python
-------------------------------

En los sistemas Unix y tipo BSD, los programas Python pueden convertirse
directamente en ejecutables, como programas del intérprete de comandos,
poniendo la linea::

   #! /usr/bin/env python3.5

...al principio del script y dándole al archivo permisos de ejecución
(asumiendo que el intérprete están en la variable de entorno :envvar:`PATH` del
usuario).  ``#!`` deben ser los primeros dos caracteres del archivo.  En
algunas plataformas, la primera línea debe terminar al estilo Unix (``'\n'``),
no como en Windows (``'\r\n'``).  Notá que el caracter numeral
``'#'`` se usa en Python para comenzar un comentario.

Se le puede dar permisos de ejecución al script usando el comando
:program:`chmod`::

.. code-block:: bash

   $ chmod +x myscript.py

En sistemas Windows, no existe la noción de "modo ejecutable".  El instalador
de Python asocia automáticamente la extensión ``.py`` con ``python.exe`` para
que al hacerle doble click a un archivo Python se corra el script.  La
extensión también puede ser ``.pyw``, en este caso se omite la ventana con la
consola que normalmente aparece.


.. _tut-startup:

El archivo de inicio interactivo
--------------------------------

Cuando usás Python en forma interactiva, suele ser útil que algunos comandos
estándar se ejecuten cada vez que el intérprete se inicia.  Podés hacer esto
configurando la variable de entorno :envvar:`PYTHONSTARTUP` con el nombre de un
archivo que contenga tus comandos de inicio.  Esto es similar al archivo
:file:`.profile` en los intérpretes de comandos de Unix.

Este archivo es solo leído en las sesiones interactivas del intérprete, no
cuando Python lee comandos de un script ni cuando :file:`/dev/tty` se explicita
como una fuente de comandos (que de otro modo se comporta como una sesión
interactiva).  Se ejecuta en el mismo espacio de nombres en el que los comandos
interactivos se ejecutan, entonces los objetos que define o importa pueden ser
usados sin cualificaciones en la sesión interactiva.  En este archivo también
podés cambiar los prompts ``sys.ps1`` y ``sys.ps2``.

Si querés leer un archivo de inicio adicional desde el directorio actual,
podés programarlo en el archivo de inicio global usando algo como ``if
os.path.isfile('.pythonrc.py'): exec(open('.pythonrc.py').read())``.  Si
querés usar el archivo de inicio en un script, tenés que hacer lo siguiente
de forma explícita en el script::

   import os
   nombrearchivo = os.environ.get('PYTHONSTARTUP')
   if nombrearchivo and os.path.isfile(nombrearchivo):
       with open(nombrearchivo) as fobj:
           archivo_inicio = fobj.read()
       exec(archivo_inicio)


.. _tut-customize:

Los módulos de customización
----------------------------

Python provee dos formas para customizarlo: :mod:`sitecustomize` y
:mod:`usercustomize`.  Para ver como funciona, necesitás primero encontrar
dónde está tu directorio para tu usuario de paquetes del sistema.  Arrancá
Python y ejecutá el siguiente código::

   >>> import site
   >>> site.getusersitepackages()
   '/home/user/.local/lib/python3.5/site-packages'

Ahora podés crear un archivo llamado :file:`usercustomize.py` en ese
directorio y poner lo que quieras en él.  Eso afectará cada ejecución de
Python, a menos que se arranque con la opción :option:`-s` para
deshabilitar esta importación automática.

:mod:`sitecustomize` funciona de la misma manera, pero normalmente lo crea
el administrador de la computadora en el directorio global de paquetes para el
sistema, y se importa antes que :mod:`usercustomize`. Para más detalles, mirá
la documentación del módulo :mod:`site`.

.. rubric:: Footnotes

.. [#] A problem with the GNU Readline package may prevent this.
