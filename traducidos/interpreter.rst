.. _tut-using:

******************************
Usando el intérprete de Python
******************************


.. _tut-invoking:

Invocando al intérprete
=======================

Por lo general, el intérprete de Python se instala en
:file:`/usr/local/bin/python3.4` en las máquinas dónde está disponible; poner
:file:`/usr/local/bin` en el camino de búsqueda de tu intérprete de comandos
Unix hace posible iniciarlo ingresando la orden:

.. code-block:: text

   python3.4

...en la terminal. [#]_ Ya que la elección del directorio dónde vivirá el
intérprete es una opción del proceso de instalación, puede estar en otros
lugares; consultá a tu Gurú Python local o administrador de sistemas. (Por
ejemplo, :file:`/usr/local/python` es una alternativa popular).

En máquinas con Windows, la instalación de Python por lo general se encuentra
en :file:`C:\\Python34`, aunque se puede cambiar durante la instalación.  Para
añadir este directorio al camino, podes ingresar la siguiente orden en el
prompt de DOS::

   set path=%path%;C:\python34

Se puede salir del intérprete con estado de salida cero ingresando el carácter
de fin de archivo (:kbd:`Control-D` en Unix, :kbd:`Control-Z` en Windows) en el
prompt primario.  Si esto no funciona, se puede salir del intérprete
ingresando: ``quit()``.

Las características para editar líneas del intérprete incluyen edición
interactiva, sustitución usando el historial y completado de código en
sistemas que soportan readline. Tal vez la forma más rápida de
detectar si las características de edición están presentes es ingresar
Control-P en el primer prompt de Python que aparezca.  Si se escucha
un beep, las características están presentes; ver Apéndice
:ref:`tut-interacting` para una introducción a las teclas.  Si no pasa
nada, o si aparece ``^P``, estas características no están disponibles;
solo vas a poder usar backspace para borrar los caracteres de la línea
actual.

La forma de operar del intérprete es parecida a la línea de comandos de
Unix: cuando se la llama con la entrada estándar conectada a una terminal
lee y ejecuta comandos en forma interactiva; cuando es llamada con un nombre de
archivo como argumento o con un archivo como entrada estándar, lee y ejecuta
un *script* del archivo.

Una segunda forma de iniciar el intérprete es ``python -c comando [arg] ...``,
que ejecuta las sentencias en *comando*, similar a la opción :option:`-c` de la
línea de comandos.  Ya que las sentencias de Python suelen tener espacios en
blanco u otros caracteres que son especiales en la línea de comandos, es
normalmente recomendado citar *comando* entre comillas dobles.

Algunos módulos de Python son también útiles como scripts.  Pueden invocarse
usando ``python -m module [arg] ...``, que ejecuta el código de *module* como
si se hubiese ingresado su nombre completo en la línea de comandos.

Cuando se usa un script, a veces es útil correr primero el script y luego
entrar al modo interactivo.  Esto se puede hacer pasándole la opción
:option:`-i` antes del nombre del script.


.. _tut-argpassing:

Pasaje de argumentos
--------------------

Cuando son conocidos por el intérprete, el nombre del script y los argumentos
adicionales son entonces convertidos a una lista de cadenas de texto asignada
a la variable ``argv`` del módulo ``sys``.  Podés acceder a esta lista
haciendo ``import sys``.  El largo de esta lista es al menos uno; cuando ningún
script o argumentos son pasados, ``sys.argv[0]`` es una cadena vacía.  Cuando
se pasa el nombre del script con ``'-'`` (lo que significa la entrada
estándar), ``sys.argv[0]`` vale ``'-'``.  Cuando se usa :option:`-c` *command*,
``sys.argv[0]`` vale ``'-c'``.  Cuando se usa :option:`-m` *module*,
``sys.argv[0]``  toma el valor del nombre completo del módulo.  Las opciones
encontradas luego de :option:`-c` *command* o :option:`-m` *module* no son
consumidas por el procesador de opciones de Python pero de todas formas
almacenadas en ``sys.argv`` para ser manejadas por el comando o módulo.


.. _tut-interactive:

Modo interactivo
----------------

Se dice que estamos usando el intérprete en modo interactivo, cuando los
comandos son leídos desde una terminal.  En este modo espera el siguiente
comando con el *prompt primario*, usualmente tres signos mayor-que (``>>>``);
para las líneas de continuación espera con el *prompt secundario*, por defecto
tres puntos (``...``).  Antes de mostrar el prompt primario, el intérprete
muestra un mensaje de bienvenida reportando su número de versión y una nota de
copyright::

   $ python3.4
   Python 3.4 (default, Mar 16 2014, 09:25:04)
   [GCC 4.8.2] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

Las líneas de continuación son necesarias cuando queremos ingresar un
constructor multilínea.  Como en el ejemplo, mirá la sentencia :keyword:`if`::

   >>> el_mundo_es_plano = True
   >>> if el_mundo_es_plano:
   ...     print("¡Tené cuidado de no caerte!")
   ...
   ¡Tené cuidado de no caerte!


.. _tut-interp:


El intérprete y su entorno
==========================

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

   #! /usr/bin/env python3.4

...al principio del script y dándole al archivo permisos de ejecución
(asumiendo que el intérprete están en la variable de entorno :envvar:`PATH` del
usuario).  ``#!`` deben ser los primeros dos caracteres del archivo.  En
algunas plataformas, la primera línea debe terminar al estilo Unix (``'\n'``),
no como en Windows (``'\r\n'``).  Notá que el caracter numeral
``'#'`` se usa en Python para comenzar un comentario.

Se le puede dar permisos de ejecución al script usando el comando
:program:`chmod`::

   $ chmod +x myscript.py

En sistemas Windows, no existe la noción de "modo ejecutable".  El instalador
de Python asocia automáticamente la extensión ``.py`` con ``python.exe`` para
que al hacerle doble click a un archivo Python se corra el script.  La
extensión también puede ser ``.pyw``, en este caso se omite la ventana con la
consola que normalmente aparece.


.. _tut-source-encoding:

Codificación del código fuente
------------------------------

Por default, los archivos fuente de Python son tratados como codificados en
UTF-8.  En ese codificación, los caracteres de la mayoría de los lenguajes
del mundo pueden ser usados simultáneamente en literales, identificadores
y comentarios, a pesar de que la biblioteca estándar usa solamente caracteres
ASCII para los identificadores, una convención que debería seguir cualquier
código que sea portable. Para mostrar estos caracteres correctamente, tu editor
debe reconocer que el archivo está en UTF-8 y usar una tipografía que soporte
todos los careacteres del archivo.

También es posible especificar una codificación distinta para los archivos
fuente.   Para hacer esto, poné una o más lineas de comentarios especiales
luego de la linea del ``#!`` para definir la codificación del archivo fuente::

   # -*- coding: encoding -*-

Con esa declaración, todo en el archivo fuente será tratado utilizando la
codificación *encoding* en lugar de UTF-8.  La lista de posibles
codificaciones se puede encontrar en la Referencia de la Biblioteca
de Python, en la sección sobre :mod:`codecs`.

Por ejemplo, si tu editor no soporta la codificación UTF-8 e insiste en usar
alguna otra, digamos Windows-1252, podés escribir::

   # -*- coding: cp-1252 -*-

y usar todos los caracteres del conjunto de Windows-1252 en los archivos
fuente.  El comentario especial de la codificación debe estar en la *primera
o segunda* linea del archivo.


.. _tut-startup:

El archivo de inicio interactivo
--------------------------------

Cuando usás Python en forma interactiva, suele ser útil que algunos comandos
estándar se ejecuten cada vez que el intérprete se inicia.  Podés hacer esto
configurando la variable de entorno :envvar:`PYTHONSTARTUP` con el nombre de un
archivo que contenga tus comandos de inicio.  Esto es similar al archivo
:file:`.profile` en los intérpretes de comandos de Unix.

.. XXX Esto probablemente debe ser puesto en un apéndice ya que la mayoría
   de las personas no usan Python interactivamente de formas no triviales.

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
       exec(open(nombrearchivo).read())


.. _tut-customize:

Los módulos de customización
----------------------------

Python provee dos formas para customizarlo: :mod:`sitecustomize` y
:mod:`usercustomize`.  Para ver como funciona, necesitás primero encontrar
dónde está tu directorio para tu usuario de paquetes del sistema.  Arrancá
Python y ejecutá el siguiente código::

   >>> import site
   >>> site.getusersitepackages()
   '/home/user/.local/lib/python3.2/site-packages'

Ahora podés crear un archivo llamado :file:`usercustomize.py` en ese
directorio y poner lo que quieras en él.  Eso afectará cada ejecución de
Python, a menos que se arranque con la opción :option:`-s` para
deshabilitar esta importación automática.

:mod:`sitecustomize` funciona de la misma manera, pero normalmente lo crea
el administrador de la computadora en el directorio global de paquetes para el
sistema, y se importa antes que :mod:`usercustomize`. Para más detalles, mirá
la documentación del módulo :mod:`site`.


.. rubric:: Footnotes

.. [#] En Unix, el intérprete de Python 3.x no se instala por default con el
   ejecutable llamado ``python`` para que no conflictúe con un ejecutable de
   Python 2.x que esté instalado simultaneamente.

.. [#] Un problema con el paquete GNU Readline puede evitar que funcione.
