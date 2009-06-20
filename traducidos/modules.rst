.. _tut-modules:

*******
Módulos
*******

Si salís del intérprete de Python y entrás de nuevo, las definiciones que
hiciste (funciones y variables) se pierden.  Por lo tanto, si querés escribir
un programa más o menos largo, es mejor que uses un editor de texto para
preparar la entrada para el interprete y ejecutarlo con ese archivo como
entrada.  Esto es conocido como crear un *guión*, o *script*.  Si tu programa
se vuelve más largo, quizás quieras separarlo en distintos archivos para un
mantenimiento más fácil.  Quizás también quieras usar una función útil que
escribiste desde distintos programas sin copiar su definición a cada programa.

Para soportar esto, Python tiene una manera de poner definiciones en un archivo
y usarlos en un script o en una instancia interactiva del intérprete.  Tal
archivo es llamado *módulo*; las definiciones de un módulo pueden ser
*importadas* a otros módulos o al módulo *principal* (la colección de variables
a las que tenés acceso en un script ejecutado en el nivel superior y en el modo
calculadora).

Un módulo es una archivo conteniendo definiciones y declaraciones de Python.
El nombre del archivo es el nombre del módulo con el sufijo :file:`.py`
agregado. Dentro de un módulo, el nombre del mismo (como una cadena) está
disponible en el valor de la variable global ``__name__``.  Por ejemplo, usá
tu editor de textos favorito para crear un archivo llamado :file:`fibo.py` en
el directorio actual, con el siguiente contenido::

   # módulo de números Fibonacci

   def fib(n):    # escribe la serie Fibonacci hasta n
       a, b = 0, 1
       while b < n:
           print b,
           a, b = b, a+b

   def fib2(n): # devuelve la serie Fibonacci hasta n
       resultado = []
       a, b = 0, 1
       while b < n:
           resultado.append(b)
           a, b = b, a+b
       return resultado

Ahora entrá al intérprete de Python e importá este módulo con la siguiente
órden::

   >>> import fibo

Esto no mete los nombres de las funciones definidas en ``fibo`` directamente
en el espacio de nombres actual; sólo mete ahí el nombre del módulo, ``fibo``.
Usando el nombre del módulo podés acceder a las funciones::

   >>> fibo.fib(1000)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987
   >>> fibo.fib2(100)
   [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
   >>> fibo.__name__
   'fibo'

Si pensás usar la función frecuentemente, podés asignarla a un nombre local::

   >>> fib = fibo.fib
   >>> fib(500)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377


.. _tut-moremodules:

Más sobre los módulos
=====================

Un módulo puede contener tanto declaraciones ejecutables como definiciones
de funciones.  Estas declaraciones están pensadas para inicializar el módulo.
Se ejecutan solamente la *primera* vez que el módulo se importa en algún
lado. [#]_

Cada módulo tiene su propio espacio de nombres, el que es usado como espacio
de nombres global por todas las funciones definidas en el módulo.  Por lo
tanto, el autor de un módulo puede usar variables globales en el módulo sin
preocuparse acerca de  conflictos con una variable global del usuario.
Por otro lado, si sabés lo que estás haciendo podés tocar las variables
globales de un módulo con la misma notación usada para referirte a sus
funciones, ``nombremodulo.nombreitem``.

Los módulos pueden importar otros módulos.  Es costumbre pero no obligatorio el
ubicar todas las declaraciones :keyword:`import` al principio del módulo (o
script, para el caso).  Los nombres de los módulos importados se ubican en el
espacio de nombres global del módulo que hace la importación.

Hay una variante de la declaración :keyword:`import` que importa los nombres de
un módulo directamente al espacio de nombres del módulo que hace la
importación.  Por ejemplo::

   >>> from fibo import fib, fib2
   >>> fib(500)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377

Esto no introduce en el espacio de nombres local el nombre del módulo desde el
cual se está importando (entonces, en el ejemplo, ``fibo`` no se define).

Hay incluso una variante para importar todos los nombres que un módulo define::

   >>> from fibo import *
   >>> fib(500)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377

Esto importa todos los nombres excepto aquellos que comienzan con un subrayado
(``_``).

.. note::

   Por razones de eficiencia, cada módulo se importa una vez por sesión del
   intérprete.  Por lo tanto, si cambiás los módulos, tenés que reiniciar el
   intérprete -- o, si es sólo un módulo que querés probar interactivamente,
   usá  :func:`reload`, por ejemplo ``reload(nombremodulo)``.


.. _tut-modulesasscripts:

Ejecutando módulos como scripts
-------------------------------

Cuando ejecutás un módulo de Python con ::

   python fibo.py <argumentos>

el código en el módulo será ejecutado, tal como si lo hubieses importado, pero
con ``__name__`` con el valor de ``"__main__"``.  Eso significa que agregando
este código al final de tu módulo::

   if __name__ == "__main__":
       import sys
       fib(int(sys.argv[1]))

podés hacer que el archivo sea utilizable tanto como script como un módulo
importable, porque el código que analiza la linea de órdenes sólo se ejecuta
si el módulo es ejecutado como archivo principal::

   $ python fibo.py 50
   1 1 2 3 5 8 13 21 34

Si el módulo se importa, ese código no se ejecuta::

   >>> import fibo
   >>>

Esto es frecuentemente usado para proveer al módulo una interfaz de usuario
conveniente, o para propósitos de prueba (ejecutar el módulo como un script
ejecuta el juego de pruebas).


.. _tut-searchpath:

El camino de búsqueda de los módulos
------------------------------------

.. index:: triple: module; search; path

Cuando se importa un módulo llamado :mod:`spam`, el intérprete busca un archivo
llamado  :file:`spam.py` en el directorio actual, y luego en la lista de
directorios especificada por la variable de entorno :envvar:`PYTHONPATH`.  Esta
tiene la misma sintáxis que la variable de shell :envvar:`PATH`, o sea, una
lista de nombres de directorios.  Cuando :envvar:`PYTHONPATH` no está
configurada, o cuando el archivo no se encuentra allí, la búsqueda continua en
un camino por default que depende de la instalación; en Unix, este es
normalmente :file:`.:/usr/lib/python`.

En realidad, los módulos se buscan en la lista de directorios dada por la
variable ``sys.path``, la cual se inicializa con el directorio que contiene al
script de entrada (o el directorio actual), :envvar:`PYTHONPATH`, y el
directorio default dependiente de la instalación. Esto permite que los
programas en Python que saben lo que están haciendo modifiquen o reemplacen el
camino de búsqueda de los módulos.  Notar que como el directorio que contiene
el script que se ejecuta está en el camino de búsqueda, es importante que el
script no tenga el mismo nombre que un módulo estándar, o Python intentará
cargar el script como un módulo cuando ese módulo se importe.  Esto
generalmente será un error.  Mirá la sección :ref:`tut-standardmodules` para
más información.


Archivos "compilados" de Python
-------------------------------

Como una importante aceleración del tiempo de arranque para programas cortos
que usan un montón de los módulos estándar, si un archivo llamado
:file:`spam.pyc` existe en el directorio donde se encuentra :file:`spam.py`, se
asume que contiene una versión ya "compilada a byte" del módulo :mod:`spam`.
La fecha y hora de modificación del archivo :file:`spam.py` usado para crar
:file:`spam.pyc` se graba en este último, y el :file:`.pyc` se ignora si estos
no coinciden.

Normally, you don't need to do anything to create the :file:`spam.pyc` file.
Whenever :file:`spam.py` is successfully compiled, an attempt is made to write
the compiled version to :file:`spam.pyc`.  It is not an error if this attempt
fails; if for any reason the file is not written completely, the resulting
:file:`spam.pyc` file will be recognized as invalid and thus ignored later.  The
contents of the :file:`spam.pyc` file are platform independent, so a Python
module directory can be shared by machines of different architectures.

Some tips for experts:

* When the Python interpreter is invoked with the :option:`-O` flag, optimized
  code is generated and stored in :file:`.pyo` files.  The optimizer currently
  doesn't help much; it only removes :keyword:`assert` statements.  When
  :option:`-O` is used, *all* :term:`bytecode` is optimized; ``.pyc`` files are
  ignored and ``.py`` files are compiled to optimized bytecode.

* Passing two :option:`-O` flags to the Python interpreter (:option:`-OO`) will
  cause the bytecode compiler to perform optimizations that could in some rare
  cases result in malfunctioning programs.  Currently only ``__doc__`` strings are
  removed from the bytecode, resulting in more compact :file:`.pyo` files.  Since
  some programs may rely on having these available, you should only use this
  option if you know what you're doing.

* A program doesn't run any faster when it is read from a :file:`.pyc` or
  :file:`.pyo` file than when it is read from a :file:`.py` file; the only thing
  that's faster about :file:`.pyc` or :file:`.pyo` files is the speed with which
  they are loaded.

* When a script is run by giving its name on the command line, the bytecode for
  the script is never written to a :file:`.pyc` or :file:`.pyo` file.  Thus, the
  startup time of a script may be reduced by moving most of its code to a module
  and having a small bootstrap script that imports that module.  It is also
  possible to name a :file:`.pyc` or :file:`.pyo` file directly on the command
  line.

* It is possible to have a file called :file:`spam.pyc` (or :file:`spam.pyo`
  when :option:`-O` is used) without a file :file:`spam.py` for the same module.
  This can be used to distribute a library of Python code in a form that is
  moderately hard to reverse engineer.

  .. index:: module: compileall

* The module :mod:`compileall` can create :file:`.pyc` files (or :file:`.pyo`
  files when :option:`-O` is used) for all modules in a directory.


.. _tut-standardmodules:

Standard Modules
================

.. index:: module: sys

Python comes with a library of standard modules, described in a separate
document, the Python Library Reference ("Library Reference" hereafter).  Some
modules are built into the interpreter; these provide access to operations that
are not part of the core of the language but are nevertheless built in, either
for efficiency or to provide access to operating system primitives such as
system calls.  The set of such modules is a configuration option which also
depends on the underlying platform For example, the :mod:`winreg` module is only
provided on Windows systems. One particular module deserves some attention:
:mod:`sys`, which is built into every Python interpreter.  The variables
``sys.ps1`` and ``sys.ps2`` define the strings used as primary and secondary
prompts::

   >>> import sys
   >>> sys.ps1
   '>>> '
   >>> sys.ps2
   '... '
   >>> sys.ps1 = 'C> '
   C> print 'Yuck!'
   Yuck!
   C>


These two variables are only defined if the interpreter is in interactive mode.

The variable ``sys.path`` is a list of strings that determines the interpreter's
search path for modules. It is initialized to a default path taken from the
environment variable :envvar:`PYTHONPATH`, or from a built-in default if
:envvar:`PYTHONPATH` is not set.  You can modify it using standard list
operations::

   >>> import sys
   >>> sys.path.append('/ufs/guido/lib/python')


.. _tut-dir:

The :func:`dir` Function
========================

The built-in function :func:`dir` is used to find out which names a module
defines.  It returns a sorted list of strings::

   >>> import fibo, sys
   >>> dir(fibo)
   ['__name__', 'fib', 'fib2']
   >>> dir(sys)
   ['__displayhook__', '__doc__', '__excepthook__', '__name__', '__stderr__',
    '__stdin__', '__stdout__', '_getframe', 'api_version', 'argv',
    'builtin_module_names', 'byteorder', 'callstats', 'copyright',
    'displayhook', 'exc_clear', 'exc_info', 'exc_type', 'excepthook',
    'exec_prefix', 'executable', 'exit', 'getdefaultencoding', 'getdlopenflags',
    'getrecursionlimit', 'getrefcount', 'hexversion', 'maxint', 'maxunicode',
    'meta_path', 'modules', 'path', 'path_hooks', 'path_importer_cache',
    'platform', 'prefix', 'ps1', 'ps2', 'setcheckinterval', 'setdlopenflags',
    'setprofile', 'setrecursionlimit', 'settrace', 'stderr', 'stdin', 'stdout',
    'version', 'version_info', 'warnoptions']

Without arguments, :func:`dir` lists the names you have defined currently::

   >>> a = [1, 2, 3, 4, 5]
   >>> import fibo
   >>> fib = fibo.fib
   >>> dir()
   ['__builtins__', '__doc__', '__file__', '__name__', 'a', 'fib', 'fibo', 'sys']

Note that it lists all types of names: variables, modules, functions, etc.

.. index:: module: __builtin__

:func:`dir` does not list the names of built-in functions and variables.  If you
want a list of those, they are defined in the standard module
:mod:`__builtin__`::

   >>> import __builtin__
   >>> dir(__builtin__)
   ['ArithmeticError', 'AssertionError', 'AttributeError', 'DeprecationWarning',
    'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False',
    'FloatingPointError', 'FutureWarning', 'IOError', 'ImportError',
    'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt',
    'LookupError', 'MemoryError', 'NameError', 'None', 'NotImplemented',
    'NotImplementedError', 'OSError', 'OverflowError',
    'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError',
    'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError',
    'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'True',
    'TypeError', 'UnboundLocalError', 'UnicodeDecodeError',
    'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError',
    'UserWarning', 'ValueError', 'Warning', 'WindowsError',
    'ZeroDivisionError', '_', '__debug__', '__doc__', '__import__',
    '__name__', 'abs', 'apply', 'basestring', 'bool', 'buffer',
    'callable', 'chr', 'classmethod', 'cmp', 'coerce', 'compile',
    'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod',
    'enumerate', 'eval', 'execfile', 'exit', 'file', 'filter', 'float',
    'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex',
    'id', 'input', 'int', 'intern', 'isinstance', 'issubclass', 'iter',
    'len', 'license', 'list', 'locals', 'long', 'map', 'max', 'min',
    'object', 'oct', 'open', 'ord', 'pow', 'property', 'quit', 'range',
    'raw_input', 'reduce', 'reload', 'repr', 'reversed', 'round', 'set',
    'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super',
    'tuple', 'type', 'unichr', 'unicode', 'vars', 'xrange', 'zip']


.. _tut-packages:

Packages
========

Packages are a way of structuring Python's module namespace by using "dotted
module names".  For example, the module name :mod:`A.B` designates a submodule
named ``B`` in a package named ``A``.  Just like the use of modules saves the
authors of different modules from having to worry about each other's global
variable names, the use of dotted module names saves the authors of multi-module
packages like NumPy or the Python Imaging Library from having to worry about
each other's module names.

Suppose you want to design a collection of modules (a "package") for the uniform
handling of sound files and sound data.  There are many different sound file
formats (usually recognized by their extension, for example: :file:`.wav`,
:file:`.aiff`, :file:`.au`), so you may need to create and maintain a growing
collection of modules for the conversion between the various file formats.
There are also many different operations you might want to perform on sound data
(such as mixing, adding echo, applying an equalizer function, creating an
artificial stereo effect), so in addition you will be writing a never-ending
stream of modules to perform these operations.  Here's a possible structure for
your package (expressed in terms of a hierarchical filesystem)::

   sound/                          Top-level package
         __init__.py               Initialize the sound package
         formats/                  Subpackage for file format conversions
                 __init__.py
                 wavread.py
                 wavwrite.py
                 aiffread.py
                 aiffwrite.py
                 auread.py
                 auwrite.py
                 ...
         effects/                  Subpackage for sound effects
                 __init__.py
                 echo.py
                 surround.py
                 reverse.py
                 ...
         filters/                  Subpackage for filters
                 __init__.py
                 equalizer.py
                 vocoder.py
                 karaoke.py
                 ...

When importing the package, Python searches through the directories on
``sys.path`` looking for the package subdirectory.

The :file:`__init__.py` files are required to make Python treat the directories
as containing packages; this is done to prevent directories with a common name,
such as ``string``, from unintentionally hiding valid modules that occur later
on the module search path. In the simplest case, :file:`__init__.py` can just be
an empty file, but it can also execute initialization code for the package or
set the ``__all__`` variable, described later.

Users of the package can import individual modules from the package, for
example::

   import sound.effects.echo

This loads the submodule :mod:`sound.effects.echo`.  It must be referenced with
its full name. ::

   sound.effects.echo.echofilter(input, output, delay=0.7, atten=4)

An alternative way of importing the submodule is::

   from sound.effects import echo

This also loads the submodule :mod:`echo`, and makes it available without its
package prefix, so it can be used as follows::

   echo.echofilter(input, output, delay=0.7, atten=4)

Yet another variation is to import the desired function or variable directly::

   from sound.effects.echo import echofilter

Again, this loads the submodule :mod:`echo`, but this makes its function
:func:`echofilter` directly available::

   echofilter(input, output, delay=0.7, atten=4)

Note that when using ``from package import item``, the item can be either a
submodule (or subpackage) of the package, or some  other name defined in the
package, like a function, class or variable.  The ``import`` statement first
tests whether the item is defined in the package; if not, it assumes it is a
module and attempts to load it.  If it fails to find it, an :exc:`ImportError`
exception is raised.

Contrarily, when using syntax like ``import item.subitem.subsubitem``, each item
except for the last must be a package; the last item can be a module or a
package but can't be a class or function or variable defined in the previous
item.


.. _tut-pkg-import-star:

Importing \* From a Package
---------------------------

.. index:: single: __all__

Now what happens when the user writes ``from sound.effects import *``?  Ideally,
one would hope that this somehow goes out to the filesystem, finds which
submodules are present in the package, and imports them all.  Unfortunately,
this operation does not work very well on Windows platforms, where the
filesystem does not always have accurate information about the case of a
filename!  On these platforms, there is no guaranteed way to know whether a file
:file:`ECHO.PY` should be imported as a module :mod:`echo`, :mod:`Echo` or
:mod:`ECHO`.  (For example, Windows 95 has the annoying practice of showing all
file names with a capitalized first letter.)  The DOS 8+3 filename restriction
adds another interesting problem for long module names.

The only solution is for the package author to provide an explicit index of the
package.  The import statement uses the following convention: if a package's
:file:`__init__.py` code defines a list named ``__all__``, it is taken to be the
list of module names that should be imported when ``from package import *`` is
encountered.  It is up to the package author to keep this list up-to-date when a
new version of the package is released.  Package authors may also decide not to
support it, if they don't see a use for importing \* from their package.  For
example, the file :file:`sounds/effects/__init__.py` could contain the following
code::

   __all__ = ["echo", "surround", "reverse"]

This would mean that ``from sound.effects import *`` would import the three
named submodules of the :mod:`sound` package.

If ``__all__`` is not defined, the statement ``from sound.effects import *``
does *not* import all submodules from the package :mod:`sound.effects` into the
current namespace; it only ensures that the package :mod:`sound.effects` has
been imported (possibly running any initialization code in :file:`__init__.py`)
and then imports whatever names are defined in the package.  This includes any
names defined (and submodules explicitly loaded) by :file:`__init__.py`.  It
also includes any submodules of the package that were explicitly loaded by
previous import statements.  Consider this code::

   import sound.effects.echo
   import sound.effects.surround
   from sound.effects import *

In this example, the echo and surround modules are imported in the current
namespace because they are defined in the :mod:`sound.effects` package when the
``from...import`` statement is executed.  (This also works when ``__all__`` is
defined.)

Note that in general the practice of importing ``*`` from a module or package is
frowned upon, since it often causes poorly readable code. However, it is okay to
use it to save typing in interactive sessions, and certain modules are designed
to export only names that follow certain patterns.

Remember, there is nothing wrong with using ``from Package import
specific_submodule``!  In fact, this is the recommended notation unless the
importing module needs to use submodules with the same name from different
packages.


Intra-package References
------------------------

The submodules often need to refer to each other.  For example, the
:mod:`surround` module might use the :mod:`echo` module.  In fact, such
references are so common that the :keyword:`import` statement first looks in the
containing package before looking in the standard module search path. Thus, the
:mod:`surround` module can simply use ``import echo`` or ``from echo import
echofilter``.  If the imported module is not found in the current package (the
package of which the current module is a submodule), the :keyword:`import`
statement looks for a top-level module with the given name.

When packages are structured into subpackages (as with the :mod:`sound` package
in the example), you can use absolute imports to refer to submodules of siblings
packages.  For example, if the module :mod:`sound.filters.vocoder` needs to use
the :mod:`echo` module in the :mod:`sound.effects` package, it can use ``from
sound.effects import echo``.

Starting with Python 2.5, in addition to the implicit relative imports described
above, you can write explicit relative imports with the ``from module import
name`` form of import statement. These explicit relative imports use leading
dots to indicate the current and parent packages involved in the relative
import. From the :mod:`surround` module for example, you might use::

   from . import echo
   from .. import formats
   from ..filters import equalizer

Note that both explicit and implicit relative imports are based on the name of
the current module. Since the name of the main module is always ``"__main__"``,
modules intended for use as the main module of a Python application should
always use absolute imports.


Packages in Multiple Directories
--------------------------------

Packages support one more special attribute, :attr:`__path__`.  This is
initialized to be a list containing the name of the directory holding the
package's :file:`__init__.py` before the code in that file is executed.  This
variable can be modified; doing so affects future searches for modules and
subpackages contained in the package.

While this feature is not often needed, it can be used to extend the set of
modules found in a package.


.. rubric:: Footnotes

.. [#] In fact function definitions are also 'statements' that are 'executed'; the
   execution enters the function name in the module's global symbol table.

