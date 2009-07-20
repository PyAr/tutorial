.. _tut-using:

******************************
Usando el Intérprete de Python
******************************


.. _tut-invoking:

Invocando al Intérprete
=======================

Por lo general, el intérprete de Python se instala en
file:`/usr/local/bin/python` en las máquinas dónde está disponible; poner
:file:`/usr/local/bin` en el camino de búsqueda de tu intérprete de comandos
Unix hace posible iniciarlo tipeando el comando::

   python

en la terminal.  Ya que la elección del directorio dónde vivirá el intérprete
es una opción del proceso de instalación, puede estar en otros lugares;
consultá a tu Gurú Python local o administrador de sistemas. (Por ejemplo,
:file:`/usr/local/python` es una alternativa popular).

En máquinas con Windows, la instalación de Python por lo general se encuentra
en :file:`C:\\Python26`, aunque se puede cambiar durante la instalación. Para
añadir este directorio al camino, puedes tipear el siguiente comando en el
prompt de DOS::

   set path=%path%;C:\python26

Se puede salir del intérprete con estado de salida cero tipeando el caracter de
fin de archivo (:kbd:`Control-D` en Unix, :kbd:`Control-Z` en Windows) en el
prompt primario. Si esto no funciona, se puede salir del intérprete tipeando el
siguiente comando: ``import sys; sys.exit()``.

Las características para editar líneas del intérprete no son muy sofisticadas.
En Unix, quien instale el intérpreté tendrá habilitado el soporte para la
biblioteca GNU readlines, que añade una edición interactiva más elaborada e
historia. Tal vez la forma más rápida de detectar si las características de
edición están presentes es tipear Control-P en el primer prompt de Python que
aparezca. Si se escucha un beep, las características están presentes; ver
Apéndice :ref:`tut-interacting` para una introducción a las teclas. Si no pasa
nada, o si aparece ``^P``, estas características no están disponibles; solo vas
a poder usar backspace para borrar los caracteres de la línea actual.

La forma de operar del intérprete es parecida a la línea de comandos de
Unix:cuando se la llama con la entrada estándar conectada a un dispostivo tty,
lee y ejecuta comandos en forma interactiva; cuando es llamada con un nombre de
archivo como argumento o con un archivo como entrada estánddar, lee y ejecuta
un *script* del archivo.

Una segunda forma de iniciar el intérprete es ``python -c command [arg] ...``,
que ejecuta las sentencias en *command*, similar a la opción :option:`-c` de la
línea de comandos. Ya que las sentencias de Python suelen tener espacios en
blanco u otros caracteres que son especiales en la línea de comandos, es mejor
citar *command* entre comillas dobles.

Algunos módulos de Python son también útiles como scripts. Pueden ser invocados 
usando ``python -m module [arg] ...``, que ejecuta el código de *module* como
si se hubiese tipeado su nombre completo en la línea de comandos.

Notá que existe una diferencia entre ``python file`` y ``python <file``.
En el último caso, la entrada solicitada por el programa, como en llamadas a 
:func:`input` y :func:`raw_input`, son satisfechas desde *file*. Ya que este
archivo ya fue leído hasta el final por el analizador antes de que el programa
empiece su ejecución, se encontrará el fin de archivo enseguida. En el primer
caso (lo que usualmente vas a querer) son satisfechas por cualquier archivo o
dispositivo que esté conectado a la entrada estándar del intérprete de Python.

Cuando se usa un script, a veces es útil correr primero el script y luego
entrar al modo interactivo. Esto se puede hacer pasándole la opción
:option:`-i` antes del nombre del script. (Esto no funciona si el script es
leido desde la entrada estándar, por la misma razón explicada en el párrafo
anterior).

.. _tut-argpassing:

Pasaje de Argumentos
--------------------

Cuando son conocidos por el intérprete, el nombre del escript y los argumentos
adicionales son entonces pasados al script en la variable ``sys.argv``,
una lista de cadenas de texto. Su logitud es al menos uno; cuando ningún script
o argumentos son pasados, ``sys.argv[0]`` es una cadena vacía. Cuando se pasa
el nombre del script con ``'-'`` (lo que significa la entrada estándar),
``sys.argv[0]`` vale ``'-'``. Cuando se usa :option:`-c` *command*,
``sys.argv[0]`` vale ``'-c'``.  Cuando se usa :option:`-m` *module*,
``sys.argv[0]``  toma el valor del nombre completo del módulo. Las opciones
encontradas luego de :option:`-c` *command* o :option:`-m` *module* no son
consumidas por el procesador de opciones de Python pero de todas formas
almacenadas en ``sys.argv`` para ser manejadas por el comando o módulo.


.. _tut-interactive:

Modo Interactivo
----------------

Se dice que estamos usando el intérprete en modo interactivo, cuando los
comandos son leídos desde una tty. En este modo espera el siguiente comando con
el *prompt primario*, usualmente tres signos mayor-que (``>>>``); para las
líneas de continuación espera con el *prompt secundario*, por defecto tres
puntos (``...``). Antes de mostrar el prompt primario, el intérprete muestra un
mensaje de bienvenida reportando su número de versión y una nota de copyright::

   python
   Python 2.6 (#1, Feb 28 2007, 00:02:06)
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

Las líneas de continuación son necesarias cuando queremos ingresar un
constructor multi-línea. Como en el ejemplo, mirá la sentencia :keyword:`if`::

   >>> el_mundo_es_plano = 1
   >>> if el_mundo_es_plano:
   ...     print "¡Tené cuidado de no caerte!"
   ... 
   ¡Tené cuidado de no caerte!


.. _tut-interp:

El Intérprete y su Entorno
==========================


.. _tut-error:

Manejo de Errores
-----------------

Cuando ocurre un error, el intérprete imprime un mensaje de error y la traza
del error. En el modo interactivo, luego retorna al prompt primario; cuando la
entrada viene de un archivo, el programa termina con código de salida distinto
a cero luego de imprimir la traza del error. (Las excepciones manejadas por una
clausula :keyword:`except` en una sentecina a :keyword:`try` no son errores en
este contexto). Algunos errores son incondicionalmente fatales y causan una
terminación con código de salida distinto de cero; esto se debe
 ainconcistencias internas o a que
el intérprete se queda sin memoria. Todos los mensajes de error se escriben en
el flujo de errores estándar; las salidas normales de comandos ejecutados se
escribe en la salida estándar.

Al tipear el caracter de interrupción (por lo general Control-C o DEL) en el
prompt primario o secundario, se cancela la entrada y retorna al promt
primario. [#]_ Tipear una interrupción mientras un comando se están ejecutando
lanza la excepción :exc:`KeyboardInterrupt`, que puede ser manejada con una
sentencia :keyword:`try`.


.. _tut-scripts:

Scripts Python Ejecutables
--------------------------

En los sistemas Unix tipo BSD, los scripts Python pueden convertirse
directamente en ejecutables, como scripts del intérprete de comandos, poniendo
la linea::

   #! /usr/bin/env python

al principio del script y dándole al archivo permisos de ejecución
(asumiendo que el intérprete están en la variable de entorno :envvar:`PATH` del
usuario).  ``#!`` deben ser los primeros dos caracteres del archivo. En algunas
plataformas, la primer línea debe terminar al estilo Unix (``'\n'``), no como
en Mac OS (``'\r'``) o Windows (``'\r\n'``).  Notá que el caracter numeral
``'#'`` se usa en Python para comenzar un comentario.

Se le puede dar permisos de ejecución al script usando el comando
:program:`chmod`::

   $ chmod +x myscript.py

En sistemas Windows, no existe la noción de "modo ejecutable". El instalador de
Python asocia automáticamente la extensión ``.py`` con ``python.exe`` para que
al hacerle doble click a un archivo Python se corra el script. La extensión
también puede ser ``.pyw``, en este caso, la ventana con la consola que
normalmente aparece es omitida.

Codificación del Código Fuente
------------------------------

Es posible utilizar una codifición distinta a ASCII en el código fuente de
Pyhton. La mejor forma de hacerlo es poner otro comentario especial enseguida
después de la línea con ``#!`` para definir la codificación::

   # -*- coding: encoding -*- 


Con esa declaración, todos los caracteres en el archivo fuente serán traducidos 
utilizando la codificación *encoding*, y será posible escribir directamente
cadenas de texto literales Unicode en la codificación seleccionada. La lista de
posibles codificaciones se puede encontrar en la Referencia de la Biblioteca de
Python, en la sección sobre :mod:`codecs`.

Por ejemplo, para esrcibir literales Unicode, incluyendo el símbolo de la
moneda Euro, se puede usar la codificación ISO-8859-15, en la que el símbolo
Euro tiene el valor 164. Este script imprimirá el valor 8364 (el código Unicode
correspondiente al símbolo Euro) y luego saldrá::

   # -*- coding: iso-8859-15 -*-

   moneda = u"€"
   print ord(moneda)

Si tu editor tiene soporte para guardar archivos como ``UTF-8`` con 
*marca de orden de byte* UTF-8 (también conocida como BOM), podés usar eso en
lugar de la declaración de codificación. IDLE lo soporta si se activa 
``Options/General/Default Source Encoding/UTF-8``. Notá que esto no funciona en
versiones antiguas de Python (2.2 y anteriores), ni por el sistema operativo en
scripts con la línea con ``#!`` (solo usado en sistemas Unix).

Usando UTF-8 (ya sea mediante BOM o la declaración de codificación), los
caracteres de la mayoría de los idiomas del mundo pueden ser usados
simultaneamente en cadenas de texto o comentarios. No se soporta usar carcteres
no-ASCII en identificadores. Para mostrar todos estos caracteres en forma
apropiada, tu editor debe reconocer que el archivo es UTF-8, y debe usar una
fuente que soporte todos los caracteres del archivo.


.. _tut-startup:

El Archivo de Inicio Interactivo
--------------------------------

Cuando usás Python en forma interactiva, suele ser útil que algunos comandos 
estándar se ejecuten cada vez que el intérprete se inicia. Podés hacer esto 
configurando la variable de entorno :envvar:`PYTHONSTARTUP` con el nombre de un
archivo que contenga tus comandos de inicio. Esto es similar al archivo
:file:`.profile` en los intérpretes de comandos de Unix.

.. XXX Esto probablemente debe ser puesto en un apéndicem ya que la mayoría
   de las personas no usan Python interactivamente de formas no triviales.

Este archivo es solo leído en las sesiones interactivas del intérprete, no
cuando Python leer comandos de un script ni cuando file:`/dev/tty` se explicita
como una fuente de comandos (que de otro modo se comporta como una sesión
interactiva). Se ejecuta en el mismo espacio de nombres en el que los comandos
interactivos se ejecutan, entonces los objetos que define o importa pueden ser
usandos sin cualificaciones en la sesión interactiva. En este archivo también
podés cambiar los prompts ``sys.ps1`` y ``sys.ps2``.

Sin querés leer un archivo de inicio adicional desde el directorio actual,
podés programarlo en el archivo de inicio global usando algo como ``if
os.path.isfile('.pythonrc.py'): execfile('.pythonrc.py')``.  Si querés usar el
archivo de inicio en un script, tenés que hacer lo siguiente en forma explífica
en el script::

   import os
   nombrearchivo = os.environ.get('PYTHONSTARTUP')
   if nombrearchivo and os.path.isfile(nombrearchivo):
       execfile(nombrearchivo)


.. rubric:: Footnotes

.. [#] Un problema con el paquete GNU Readline puede evitar que funcione.
