.. _tut-using:

*****************************
Usando el Intérprete de Python
*****************************


.. _tut-invoking:

Invocando al Intérprete
========================

Por lo general, el intérprete de Python se instala en file:`/usr/local/bin/python` en las
máquinas dónde está disponible; poner :file:`/usr/local/bin` en el camino de búsqueda
de tu intérprete de comandos Unix hace posible iniciarlo tipeando el comando::

   python

en la terminal.  Ya que la elección del directorio dónde vivirá el intérprete es una
opción del proceso de instalación, puede estar en otros lugares; consultá a tu Gurú
Python local o administrador de sistemas. (Por ejemplo, :file:`/usr/local/python` es una
alternativa popular).

En máquinas con Windows, la instalación de Python por lo general se encuentra en
:file:`C:\\Python26`, aunque se puede cambiar durante la instalación. Para añadir este
directorio al camino, puedes tipear el siguiente comando en el prompt de DOS::

   set path=%path%;C:\python26

Se puede salir del intérprete con estado de salida cero tipeando el caracter de fin
de archivo (:kbd:`Control-D` en Unix, :kbd:`Control-Z` en Windows) en el prompt
primario. Si esto no funciona, se puede salir del intérprete tipeando el siguiente 
comando: ``import sys; sys.exit()``.

Las características para editar líneas del intérprete no son muy sofisticadas.
En Unix, quien instale el intérpreté tendrá habilitado el soporte para la biblioteca
GNU readlines, que añade una edición interactiva más elaborada e historia. Tal vez la
forma más rápida de detectar si las características de edición están presentes es 
tipear Control-P en el primer prompt de Python que aparezca. Si se escucha un beep,
las características están presentes; ver Apéndice :ref:`tut-interacting` para una 
introducción a las teclas. Si no pasa nada, o si aparece ``^P``, estas características
no están disponibles; solo vas a poder usar backspace para borrar los caracteres de la
línea actual.

La forma de operar del intérprete es parecida a la línea de comandos de Unix: cuando
se la llama con la entrada estándar conectada a un dispostivo tty, lee y ejecuta
comandos en forma interactiva; cuando es llamada con un nombre de archivo como
argumento o con un archivo como entrada estánddar, lee y ejecuta un *script* del
archivo.

Una segunda forma de iniciar el intérprete es ``python -c command [arg] ...``,
que ejecuta las sentencias en *command*, similar a la opción :option:`-c` de la línea
de comandos. Ya que las sentencias de Python suelen tener espacios en blanco u otros
caracteres que son especiales en la línea de comandos, es mejor citar *command* 
entre comillas dobles.

Algunos módulos de Python son también útiles como scripts. Pueden ser invocados 
usando ``python -m module [arg] ...``, que ejecuta el código de *module* como si se
hubiese tipeado su nombre completo en la línea de comandos.

Notá que existe una diferencia entre ``python file`` y ``python <file``.
En el último caso, la entrada solicitada por el programa, como en llamadas a 
:func:`input` y :func:`raw_input`, son satisfechas desde *file*. Ya que este archivo ya 
fue leído hasta el final por el analizador antes de que el programa empiece su
ejecución, se encontrará el fin de archivo enseguida. En el primer caso (lo
que usualmente vas a querer) son satisfechas por cualquier archivo o dispositivo que 
esté conectado a la entrada estándar del intérprete de Python.

Cuando se usa un script, a veces es útil correr primero el script y luego entrar al modo
interactivo. Esto se puede hacer pasándole la opción :option:`-i` antes del nombre del
script. (Esto no funciona si el script es leido desde la entrada estándar, por la misma
razón explicada en el párrafo anterior).

.. _tut-argpassing:

Argument Passing
----------------

When known to the interpreter, the script name and additional arguments
thereafter are passed to the script in the variable ``sys.argv``, which is a
list of strings.  Its length is at least one; when no script and no arguments
are given, ``sys.argv[0]`` is an empty string.  When the script name is given as
``'-'`` (meaning  standard input), ``sys.argv[0]`` is set to ``'-'``.  When
:option:`-c` *command* is used, ``sys.argv[0]`` is set to ``'-c'``.  When
:option:`-m` *module* is used, ``sys.argv[0]``  is set to the full name of the
located module.  Options found after  :option:`-c` *command* or :option:`-m`
*module* are not consumed  by the Python interpreter's option processing but
left in ``sys.argv`` for  the command or module to handle.


.. _tut-interactive:

Interactive Mode
----------------

When commands are read from a tty, the interpreter is said to be in *interactive
mode*.  In this mode it prompts for the next command with the *primary prompt*,
usually three greater-than signs (``>>>``); for continuation lines it prompts
with the *secondary prompt*, by default three dots (``...``). The interpreter
prints a welcome message stating its version number and a copyright notice
before printing the first prompt::

   python
   Python 2.6 (#1, Feb 28 2007, 00:02:06)
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

Continuation lines are needed when entering a multi-line construct. As an
example, take a look at this :keyword:`if` statement::

   >>> the_world_is_flat = 1
   >>> if the_world_is_flat:
   ...     print "Be careful not to fall off!"
   ... 
   Be careful not to fall off!


.. _tut-interp:

The Interpreter and Its Environment
===================================


.. _tut-error:

Error Handling
--------------

When an error occurs, the interpreter prints an error message and a stack trace.
In interactive mode, it then returns to the primary prompt; when input came from
a file, it exits with a nonzero exit status after printing the stack trace.
(Exceptions handled by an :keyword:`except` clause in a :keyword:`try` statement
are not errors in this context.)  Some errors are unconditionally fatal and
cause an exit with a nonzero exit; this applies to internal inconsistencies and
some cases of running out of memory.  All error messages are written to the
standard error stream; normal output from executed commands is written to
standard output.

Typing the interrupt character (usually Control-C or DEL) to the primary or
secondary prompt cancels the input and returns to the primary prompt. [#]_
Typing an interrupt while a command is executing raises the
:exc:`KeyboardInterrupt` exception, which may be handled by a :keyword:`try`
statement.


.. _tut-scripts:

Executable Python Scripts
-------------------------

On BSD'ish Unix systems, Python scripts can be made directly executable, like
shell scripts, by putting the line ::

   #! /usr/bin/env python

(assuming that the interpreter is on the user's :envvar:`PATH`) at the beginning
of the script and giving the file an executable mode.  The ``#!`` must be the
first two characters of the file.  On some platforms, this first line must end
with a Unix-style line ending (``'\n'``), not a Mac OS (``'\r'``) or Windows
(``'\r\n'``) line ending.  Note that the hash, or pound, character, ``'#'``, is
used to start a comment in Python.

The script can be given an executable mode, or permission, using the
:program:`chmod` command::

   $ chmod +x myscript.py

On Windows systems, there is no notion of an "executable mode".  The Python
installer automatically associates ``.py`` files with ``python.exe`` so that
a double-click on a Python file will run it as a script.  The extension can
also be ``.pyw``, in that case, the console window that normally appears is
suppressed.


Source Code Encoding
--------------------

It is possible to use encodings different than ASCII in Python source files. The
best way to do it is to put one more special comment line right after the ``#!``
line to define the source file encoding::

   # -*- coding: encoding -*- 


With that declaration, all characters in the source file will be treated as
having the encoding *encoding*, and it will be possible to directly write
Unicode string literals in the selected encoding.  The list of possible
encodings can be found in the Python Library Reference, in the section on
:mod:`codecs`.

For example, to write Unicode literals including the Euro currency symbol, the
ISO-8859-15 encoding can be used, with the Euro symbol having the ordinal value
164.  This script will print the value 8364 (the Unicode codepoint corresponding
to the Euro symbol) and then exit::

   # -*- coding: iso-8859-15 -*-

   currency = u"€"
   print ord(currency)

If your editor supports saving files as ``UTF-8`` with a UTF-8 *byte order mark*
(aka BOM), you can use that instead of an encoding declaration. IDLE supports
this capability if ``Options/General/Default Source Encoding/UTF-8`` is set.
Notice that this signature is not understood in older Python releases (2.2 and
earlier), and also not understood by the operating system for script files with
``#!`` lines (only used on Unix systems).

By using UTF-8 (either through the signature or an encoding declaration),
characters of most languages in the world can be used simultaneously in string
literals and comments.  Using non-ASCII characters in identifiers is not
supported. To display all these characters properly, your editor must recognize
that the file is UTF-8, and it must use a font that supports all the characters
in the file.


.. _tut-startup:

The Interactive Startup File
----------------------------

When you use Python interactively, it is frequently handy to have some standard
commands executed every time the interpreter is started.  You can do this by
setting an environment variable named :envvar:`PYTHONSTARTUP` to the name of a
file containing your start-up commands.  This is similar to the :file:`.profile`
feature of the Unix shells.

.. XXX This should probably be dumped in an appendix, since most people
   don't use Python interactively in non-trivial ways.

This file is only read in interactive sessions, not when Python reads commands
from a script, and not when :file:`/dev/tty` is given as the explicit source of
commands (which otherwise behaves like an interactive session).  It is executed
in the same namespace where interactive commands are executed, so that objects
that it defines or imports can be used without qualification in the interactive
session. You can also change the prompts ``sys.ps1`` and ``sys.ps2`` in this
file.

If you want to read an additional start-up file from the current directory, you
can program this in the global start-up file using code like ``if
os.path.isfile('.pythonrc.py'): execfile('.pythonrc.py')``.  If you want to use
the startup file in a script, you must do this explicitly in the script::

   import os
   filename = os.environ.get('PYTHONSTARTUP')
   if filename and os.path.isfile(filename):
       execfile(filename)


.. rubric:: Footnotes

.. [#] A problem with the GNU Readline package may prevent this.

