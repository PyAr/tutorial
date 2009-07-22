.. _tut-interacting:

*********************************************************
Edición de Entrada Interactiva y Sustitución de Historial
*********************************************************

Algunas versiones del intérprete de Python permiten editar la línea de entrada
actual, y sustituir en base al historial, de forma similar a las capacidades
del intérprete de comandos Korn y el GNU bash. Esto se implementa con la
biblioteca *GNU Readline*, que soporta edición al estilo de Emacs y al estilo
de vi. Esta biblioteca tiene su propia documentación que no duplicaré aquí;
pero la funcionalidad básica es fácil de explicar. La edición interactiva y
el historial aquí descriptos están disponibles como opcionales en las versiones
para Unix y Cygwin del intérprete.

Este capítulo *no* documenta las capacidades de edición del paquete PythonWin de
Mark Hammond, ni del entorno IDLE basado en Tk que se distribuye con Python.
El historial de línea de comandos que funciona en pantallas de DOS en NT y 
algunas otras variantes de DOS y Windows es también una criatura diferente.

.. _tut-lineediting:

Edición de Línea
================

De estar soportada, la edición de línea de entrada se activa en cuanto el
intérprete muestra un símbolo de espera de ordenes primario o secundario. La
línea activa puede editarse usando los caracteres de control convencionales
de Emacs. De estos, los más importantes son:
:kbd:`C-A` (Ctrl-A) mueve el cursor al comienzo de la línea, :kbd:`C-E`
al final, :kbd:`C-B` lo mueve una posición a la izquierda, :kbd:`C-F` a la
derecha. La tecla de retroceso (Backspace) borra el caracter a la izquierda
del cursor, :kbd:`C-D` el caracter a su derecha. :kbd:`C-K` corta el resto de la
línea a la derecha del cursor, :kbd:`C-Y` pega de vuelta la última cadena cortada.
:kbd:`C-underscore` deshace el último cambio hecho; puede repetirse para obtener
un efecto acumulativo.

.. _tut-history:

Sustitución de historial
========================

La sustitución de historial funciona de la siguiente manera: todas las líneas
ingresadas y no vacías se almacenan en una memoria intermedia, y cuando se te
pide una nueva línea, estás posicionado en una linea nueva al final de esta
memoria. :kbd:`C-P` se mueve una línea hacia arriba (es decir, hacia atrás) en
el historial, :kbd:`C-N` se mueve una línea hacia abajo. Cualquier línea en el
historial puede editarse; aparecerá un asterisco adelante del indicador de
entrada para marcar una línea como editada. Presionando la tecla :kbd:`Return` 
(Intro) se pasa la línea activa al intérprete. :kbd:`C-R` inicia una búsqueda
incremental hacia atrás, :kbd:`C-S` inicia una búsqueda hacia adelante.

.. _tut-keybindings:

Atajos de teclado
=================

Los atajos de teclado y algunos otros parámetros de la biblioteca Readline se
pueden personalizar poniendo comandos en un archivo de inicialización llamado
:file:`~/.inputrc`.  Los atajos de teclado tienen la forma ::

   nombre-de-tecla: nombre-de-función

o ::

   "cadena": nombre-de-función

y se pueden configurar opciones con ::

   set nombre-opción valor

Por ejemplo::

   # Prefiero edición al estilo vi:
   set editing-mode vi

   # Editar usando sólo un renglón:
   set horizontal-scroll-mode On

   # Reasociar algunas teclas:
   Meta-h: backward-kill-word
   "\C-u": universal-argument
   "\C-x\C-r": re-read-init-file

Observa que la asociación por omisión para la tecla :kbd:`Tab` en Python es
insertar un caracter  :kbd:`Tab` (tabulación horizontal) en vez de la función
por defecto de Readline de completar nombres de archivo. Si insistes, puedes
redefinir esto poniendo ::

   Tab: complete

en tu :file:`~/.inputrc`.  (Desde luego, esto hace más difícil escribir líneas
de continuación indentadas si estás acostumbrado a usar :kbd:`Tab` para tal
propósito.)

.. index::
   module: rlcompleter
   module: readline

Hay disponible opcionalmente completado automático de variables y nombres de
módulos. Para activarlo en el modo interactivo del intérprete, agrega lo
siguiente a tu archivo de arranque: [#]_  ::

   import rlcompleter, readline
   readline.parse_and_bind('tab: complete')

Esto asocia la tecla :kbd:`Tab` a la función de completado, con lo cual presionar
la tecla 
:kbd:`Tab` dos veces sugerirá valores para completar; se fija en nombres de
instrucciones Python, las variables locales del momento, y los nombres de
módulos disponibles. Para expresiones con puntos como ``string.a``, evaluará
la expresión hasta el último ``'.'`` y luego sugerirá opciones a completar de
los atributos de el objeto resultante. Tenga en cuenta que esto puede ejecutar
código definido por la aplicación si un objeto con un método :meth:`__getattr__`
forma parte de la expresión.

Un archivo de inicialización con más capacidades podría ser como este ejemplo.
Observa que éste borra los nombres que crea una vez que no se necesitan más;
esto se hace debido a que el archivo de inicialización se ejecuta en el mismo
espacio de nombres que los comandos interactivos, y borrar los nombres evita
que se produzcan efectos colaterales en el entorno interactivo. Tal vez te
resulte cómodo mantener algunos de los módulos importados, tales como :mod:`os`,
que usualmente acaban siendo necesarios en la mayoría de las sesiones con el
intérprete. ::

   # Añadir auto-completado y almacenamiento de archivo de histórico a tu
   # intérprete de Python interactivo. Requiere Python 2.0+, y readline.
   # El autocompletado esta ligado a la tecla Esc por defecto (puedes
   # modificarlo - lee la documentación de readline).
   #
   # Guarda este archivo en ~/.pystartup, y configura una variable de inicio
   # para que lo apunte: en bash "export PYTHONSTARTUP=/home/usuario/.pystartup".
   #
   # Ten en cuenta que PYTHONSTARTUP *no* expande "~", así que debes poner
   # la ruta completa a tu directorio personal.

   import atexit
   import os
   import readline
   import rlcompleter

   historyPath = os.path.expanduser("~/.pyhistory")

   def save_history(historyPath=historyPath):
       import readline
       readline.write_history_file(historyPath)

   if os.path.exists(historyPath):
       readline.read_history_file(historyPath)

   atexit.register(save_history)
   del os, atexit, readline, rlcompleter, save_history, historyPath


.. _tut-commentary:

Comentario
==========

Esta funcionalidad es un paso enorme hacia adelante comparado con versiones
anteriores del interprete; de todos modos, quedan pendientes algunos deseos:
sería bueno si la indentación correcta se sugiriera en las lineas de
continuación (el parser sabe si se requiere una indentación a continuación).
El mecanismo de completado podría usar la tabla de símbolos del intérprete.
Un comando para verificar (o incluso sugerir) coincidencia de paréntesis,
comillas, etc. también sería útil.

.. rubric:: Footnotes

.. [#] Python ejecutará el contenido de un archivo indicado por la variable de
   entorno :envvar:`PYTHONSTARTUP` cuando inicies un intérprete interactivo.

