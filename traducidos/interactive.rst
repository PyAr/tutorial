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
historial puede editarse; aparecera un asterisco adelante del indicador de
entrada para marcar una línea como editada. Presionando la tecla :kbd:`Return` 
(Intro) se pasa la líne activa al intérprete. :kbd:`C-R` inicia una búsqueda
incremental hacia atrás, :kbd:`C-S` inicia una búsqueda hacia adelante.

.. _tut-keybindings:

Atajos de teclado
=================

Los atajos de teclado y algunos otros parámetros de la biblioteca Readlina se
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

Observa que la asociación por omision para la tecla :kbd:`Tab` en Python es
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
:kbd:`Tab` dos veces sugerira valores para completar; se fija en nombres de
instrucciones Python, las variables locales del momento, y los nombres de
módulos disponibles. Para expresiones con puntos como ``string.a``, evaluará
la expresión hasta el último ``'.'`` y luego sugerirá opciones a completar de
los atributos de el objeto resultante. Tenga en cuenta que esto puede ejecutar
código definido por la aplicación si un objeto con un método :meth:`__getattr__`
forma parte de la expresión.

A more capable startup file might look like this example.  Note that this
deletes the names it creates once they are no longer needed; this is done since
the startup file is executed in the same namespace as the interactive commands,
and removing the names avoids creating side effects in the interactive
environment.  You may find it convenient to keep some of the imported modules,
such as :mod:`os`, which turn out to be needed in most sessions with the
interpreter. ::

   # Add auto-completion and a stored history file of commands to your Python
   # interactive interpreter. Requires Python 2.0+, readline. Autocomplete is
   # bound to the Esc key by default (you can change it - see readline docs).
   #
   # Store the file in ~/.pystartup, and set an environment variable to point
   # to it:  "export PYTHONSTARTUP=/home/user/.pystartup" in bash.
   #
   # Note that PYTHONSTARTUP does *not* expand "~", so you have to put in the
   # full path to your home directory.

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

Commentary
==========

This facility is an enormous step forward compared to earlier versions of the
interpreter; however, some wishes are left: It would be nice if the proper
indentation were suggested on continuation lines (the parser knows if an indent
token is required next).  The completion mechanism might use the interpreter's
symbol table.  A command to check (or even suggest) matching parentheses,
quotes, etc., would also be useful.


.. rubric:: Footnotes

.. [#] Python will execute the contents of a file identified by the
   :envvar:`PYTHONSTARTUP` environment variable when you start an interactive
   interpreter.

