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
orden::

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

...el código en el módulo será ejecutado, tal como si lo hubieses importado,
pero con ``__name__`` con el valor de ``"__main__"``.  Eso significa que
agregando este código al final de tu módulo::

   if __name__ == "__main__":
       import sys
       fib(int(sys.argv[1]))

...podés hacer que el archivo sea utilizable tanto como script como un módulo
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
asume que contiene una versión ya "compilada a byte" del módulo :mod:`spam` (lo
que se denomina *bytecode*).  La fecha y hora de modificación del archivo
:file:`spam.py` usado para crear :file:`spam.pyc` se graba en este último, y
el :file:`.pyc` se ignora si estos no coinciden.

Normalmente, no necesitás hacer nada para crear el archivo :file:`spam.pyc`.
Siempre que el se compile satisfactoriamente el :file:`spam.py`, se hace un
intento de escribir la versión compilada al :file:`spam.pyc`. No es un error
si este intento falla, si por cualquier razón el archivo no se escribe
completamente, el archivo :file:`spam.pyc` resultante se reconocerá como
inválido luego.  El contenido del archivo :file:`spam.pyc` es independiente de
la plataforma, por lo que un directorio de módulos puede ser compartido por
máquinas de diferentes arquitecturas.

Algunos consejos para expertos:

* Cuando se invoca el intérprete de Python con la opción :option:`-O`, se
  genera código optimizado que se almacena en archivos :file:`.pyo`.  El
  optimizador actualmente no ayuda mucho; sólo remueve las declaraciones
  :keyword:`assert`.  Cuando se usa :option:`-O`, se optimiza *todo* el
  :term:`bytecode`; se ignoran los archivos ``.pyc`` y los archivos ``.py``
  se compilan a bytecode optimizado.

* Pasando dos opciones :option:`-O` al intérprete de Python (:option:`-OO`)
  causará que el compilador realice optimizaciones que en algunos raros casos
  podría resultar en programas que funcionen incorrectamente. Actualmente,
  solamente se remueven del bytecode a las cadenas ``__doc__``, resultando en
  archivos :file:`.pyo` más compactos.  Ya que algunos programan necesitan
  tener disponibles estas cadenas, sólo deberías usar esta opción si sabés lo
  que estás haciendo.

* Un programa no corre más rápido cuando se lee de un archivo :file:`.pyc` o
  :file:`.pyo` que cuando se lee del :file:`.py`; lo único que es más rápido
  en los archivos :file:`.pyc` o :file:`.pyo` es la velocidad con que se
  cargan.

* Cuando se ejecuta un script desde la linea de órdenes, nunca se escribe el
  bytecode del script a los archivos :file:`.pyc` o :file:`.pyo`.  Por lo
  tanto, el tiempo de comienzo de un script puede reducirse moviendo la mayor
  parte de su códugo a un módulo y usando un pequeño script de arranque que
  importe el módulo.  También es posible nombrar a los archivos :file:`.pyc` o
  :file:`.pyo` directamente desde la linea de órdenes.

* Es posible tener archivos llamados :file:`spam.pyc` (o :file:`spam.pyo`
  cuando se usa la opción :option:`-O`) sin un archivo :file:`spam.py` para
  el mismo módulo.  Esto puede usarse para distribuir el código de una
  biblioteca de python en una forma que es moderadamente difícil de hacerle
  ingeniería inversa.

  .. index:: module: compileall

* El módulo :mod:`compileall` puede crear archivos :file:`.pyc` (o archivos
  :file:`.pyo` cuando se usa la opción :option:`-O`) para todos los módulos
  en un directorio.


.. _tut-standardmodules:

Módulos estándar
================

.. index:: module: sys

Python viene con una biblioteca de módulos estándar, descrita en un documento
separado, la Referencia de la Biblioteca de Python (de aquí en más, "Referencia
de la Biblioteca").  Algunos módulos se integran en el intérprete; estos
proveen acceso a operaciones que no son parte del núcleo del lenguaje pero que
sin embargo están integrados, tanto por eficiencia como para proveer acceso a
primitivas del sistema operativo, como llamadas al sistema.  El conjunto de
tales módulos es una opción de configuración el cual también depende de la
plataforma subyacente.  Por ejemplo, el módulo :mod:`winreg` sólo se provee
en sistemas Windows.  Un módulo en particular merece algo de atención:
:mod:`sys`, el que está integrado en todos los intérpretes de Python.  Las
variables ``sys.ps1`` y ``sys.ps2`` definen las cadenas usadas como cursores
primarios y secundarios::

   >>> import sys
   >>> sys.ps1
   '>>> '
   >>> sys.ps2
   '... '
   >>> sys.ps1 = 'C> '
   C> print 'Yuck!'
   Yuck!
   C>


Estas dos variables están solamente definidas si el intérprete está en modo interactivo.

La variable  ``sys.path`` es una lista de cadenas que determinan el camino de
búsqueda del intérprete para los módulos.  Se inicializa por omisión a un
camino tomado de la variable de entorno :envvar:`PYTHONPATH`, o a un valor
predefinido en el intérprete si :envvar:`PYTHONPATH` no está configurada.  Lo
podés modificar usando las operaciones estándar de listas::

   >>> import sys
   >>> sys.path.append('/ufs/guido/lib/python')


.. _tut-dir:

La función :func:`dir`
======================

La función integrada :func:`dir` se usa par encontrar que nombres define un
módulo.  Devuelve una lista ordenada de cadenas::

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

Sin argumentos, :func:`dir` lista los nombres que tenés actualmente definidos::

   >>> a = [1, 2, 3, 4, 5]
   >>> import fibo
   >>> fib = fibo.fib
   >>> dir()
   ['__builtins__', '__doc__', '__file__', '__name__', 'a', 'fib', 'fibo', 'sys']

Notá que lista todos los tipos de nombres: variables, módulos, funciones, etc.

.. index:: module: __builtin__

:func:`dir` no lista los nombres de las funciones y variables integradas.  Si
querés una lista de esos, están definidos en el módulo estándar
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

Paquetes
========

Los paquetes son una manera de estructurar los espacios de nombres de Python
usando "nombres de módulos con puntos".  Por ejemplo, el nombre de módulo
:mod:`A.B` designa un submódulo llamado ``B`` en un paquete llamado ``A``.
Tal como el uso de módulos evita que los autores de diferentes módulos tengan
que preocuparse de los respectivos nombres de variables globales, el uso de
nombres de módulos con puntos evita que los autores de paquetes de muchos
módulos, como NumPy o la Biblioteca de Imágenes de Python (Python Imaging
Library, o PIL), tengan que preocuparse de los respectivos nombres de módulos.

Suponete que querés designar una colección de módulos (un "paquete") para el
manejo uniforme de archivos y datos de sonidos.  Hay diferentes formatos de
archivos de sonido (normalmente reconocidos por su extensión, por ejemplo:
:file:`.wav`, :file:`.aiff`, :file:`.au`), por lo que tenés que crear y
mantener una colección siempre creciente de módulos para la conversión entre
los distintos formatos de archivos.  Hay muchas operaciones diferentes que
quizás quieras ejecutar en los datos de sonido (como mezclarlos, añadir eco,
aplicar una función ecualizadora, crear un efecto estéreo artificial), por lo
que ademas estarás escribiendo una lista sin fin de módulos para realizar
estas operaciones.  Aquí hay una posible estructura para tu paquete (expresados
en términos de un sistema jerárquico de archivos)::

   sound/                          Paquete superior
         __init__.py               Inicializa el paquete de sonido
         formats/                  Subpaquete para conversiones de formato
                 __init__.py
                 wavread.py
                 wavwrite.py
                 aiffread.py
                 aiffwrite.py
                 auread.py
                 auwrite.py
                 ...
         effects/                  Subpaquete para efectos de sonido
                 __init__.py
                 echo.py
                 surround.py
                 reverse.py
                 ...
         filters/                  Subpaquete para filtros
                 __init__.py
                 equalizer.py
                 vocoder.py
                 karaoke.py
                 ...

Al importar el paquete, Python busca a través de los directorios en
``sys.path``, buscando el subdirectorio del paquete.

Los archivos :file:`__init__.py` se necesitan para hacer que Python trate
los directorios como que contienen paquetes; esto se hace para prevenir
directorios con un nombre común, como ``string``, de esconder sin intención
a módulos válidos que se suceden luego en el camino de búsqueda de módulos.
En el caso más simple, :file:`__init__.py`  puede ser solamente un archivo
vacío, pero también puede ejecutar código de inicialización para el paquete
o configurar la variable ``__all__``, descrita luego.

Los usuarios del paquete pueden importar módulos individuales del mismo, por
ejemplo::

   import sound.effects.echo

Esto carga el submódulo :mod:`sound.effects.echo`.  Debe hacerse referencia al
mismo con el nombre completo. ::

   sound.effects.echo.echofilter(input, output, delay=0.7, atten=4)

Otra alternativa para importar el submódulos es::

   from sound.effects import echo

Esto también carga el submódulo :mod:`echo`, lo deja disponible sin su prefijo
de paquete, por lo que puede usarse así::

   echo.echofilter(input, output, delay=0.7, atten=4)

Otra variación más es importar la función o variable deseadas directamente::

   from sound.effects.echo import echofilter

De nuevo, esto carga el submódulo :mod:`echo`, pero deja directamente
disponible a la función :func:`echofilter`::

   echofilter(input, output, delay=0.7, atten=4)

Notá que al usar ``from package import item`` el ítem puede ser tanto un
submódulo (o subpaquete) del paquete, o algún otro nombre definido en el
paquete, como una función, clase, o variable.  La declaración ``import``
primero verifica si el ítem está definido en el paquete; si no, asume que es un
módulo y trata de cargarlo.  Si no lo puede encontrar, se genera una excepción
:exc:`ImportError`.

Por otro lado, cuando se usa la sintaxis como
``import item.subitem.subsubitem``, cada ítem excepto el último debe ser un
paquete; el mismo puede ser un módulo o un paquete pero no puede ser una clase,
función o variable definida en el ítem previo.


.. _tut-pkg-import-star:

Importando \* desde un paquete
------------------------------

.. index:: single: __all__

Ahora, ¿qué sucede cuando el usuario escribe ``from sound.effects import *``?
Idealmente, uno esperaría que esto de alguna manera vaya al sistema de
archivos, encuentre cuales submódulos están presentes en el paquete, y los
importe a todos.  Desafortunadamente, esta operación no trabaja muy bien en
las plataformas Windows, donde el sistema de archivos no siempre tiene
información precisa sobre mayúsculas y minúsculas.  En estas plataformas,
no hay una manera garantizada de saber si el archivo `ECHO.PY` debería
importarse como el módulo :mod:`echo`, :mod:`Echo` o :mod:`ECHO`. (Por ejemplo,
Windows 95 tiene la molesta costumbre de mostrar todos los nombres de archivos
con la primer letra en mayúsculas.)  La restricción de DOS de los nombres de
archivos con la forma 8+3 agrega otro problema interesante para los nombres
de módulos largos.

La única solución es que el autor del paquete provea un índice explícito del
paquete.  La declaración ``import`` usa la siguiente convención: si el código
del :file:`__init__.py` de un paquete define una lista llamada ``__all__``, se
toma como la lista de los nombres de módulos que deberían ser importados cuando
se hace ``from package import *``.  Es tarea del autor del paquete mantener
actualizada esta lista cuando se libera una nueva versión del paquete.  Los
autores de paquetes podrían decidir no soportarlo, si no ven un uso para
importar \* en sus paquetes.  Por ejemplo, el archivo
:file:`sounds/effects/__init__.py` podría contener el siguiente código::

   __all__ = ["echo", "surround", "reverse"]

Esto significaría que ``from sound.effects import *`` importaría esos tres
submódulos del paquete :mod:`sound`.


Si no se define ``__all__``, la declaración ``from sound.effects import *``
*no* importa todos los submódulos del paquete :mod:`sound.effects` al espacio
de nombres actual; sólo se asegura que se haya importado el paquete
:mod:`sound.effects` (posiblemente ejecutando algún código de inicialización
que haya en :file:`__init__.py`) y luego importa aquellos nombres que estén
definidos en el paquete.  Esto incluye cualquier nombre definido (y submódulos
explícitamente cargados) por :file:`__init__.py`.  También incluye cualquier
submódulo del paquete que pudiera haber sido explícitamente cargado por
declaraciones ``import`` previas.  Considerá este código::

   import sound.effects.echo
   import sound.effects.surround
   from sound.effects import *

En este ejemplo, los módulos *echo* y *surround* se importan en el espacio de
nombre actual porque están definidos en el paquete :mod:`sound.effects` cuando
se ejecuta la declaración ``from...import``.  (Esto también funciona cuando se
define ``__all__``).

Notá que en general la práctica de importar ``*`` desde un módulo o paquete no
se recomienda, ya que frecuentemente genera un código con mala legibilidad.
Sin embargo, está bien usarlo para ahorrar tecleo en sesiones interactivas,
y algunos módulos están diseñados para exportar sólo nombres que siguen
ciertos patrones.

Recordá que no está mal usar ``from Package import specific_submodule``!  De
hecho, esta notación se recomienda a menos que el módulo que estás importando
necesite usar submódulos con el mismo nombre desde otros paquetes.


Referencias internas en paquetes
--------------------------------

Los submódulos frecuentemente necesitan referirse unos a otros.  Por ejemplo,
el módulo :mod:`surround` quizás necesite usar el módulo :mod:`echo` module.
De hecho, tales referencias son tan comunes que la declaración
:keyword:`import` primero mira en el paquete actual antes de mirar en el camino
estándar de búsqueda de módulos.  Por lo tanto, el módulo :mod:`surround` puede
simplemente hacer ``import echo`` o ``from echo import echofilter``.  Si el
módulo importado no se encuentra en el paquete actual (el paquete del cual el
módulo actual es un submódulo), la declaración :keyword:`import` busca en el
nivel superior por un módulo con el nombre dado.

Cuando se estructuran los paquetes en subpaquetes (como en el ejemplo
:mod:`sound`), podés usar ``import`` absolutos para referirte a
submódulos de paquetes hermanos.  Por ejemplo, si el módulo
:mod:`sound.filters.vocoder` necesita usar el módulo :mod:`echo` en el paquete
:mod:`sound.effects`, puede hacer ``from sound.effects import echo``.

Desde Python 2.5, además de los ``import`` relativos implícitos descritos
arriba, podés escribir ``import`` relativos explícitos con la declaración de la
forma ``from module import name``.  Estos ``import`` relativos explícitos usan
puntos adelante para indicar los paquetes actual o padres involucrados en el
``import`` relativo. En el ejemplo :mod:`surround`, podrías hacer::

   from . import echo
   from .. import formats
   from ..filters import equalizer

Notá que ambos ``import``, relativos explícitos e implícitos, se basan en el
nombre del módulo actual.  Ya que el nombre del módulo principal es siempre
``"__main__"``,  los módulos pensados para usarse como módulo principal de una
aplicación Python siempre deberían usar ``import`` absolutos.


Paquetes en múltiple directorios
--------------------------------

Los paquetes soportan un atributo especial más, :attr:`__path__`.  Este
se inicializa, antes de que el código en ese archivo se ejecute, a una lista
que contiene el nombre del directorio donde está el paquete.  Esta variable
puede modificarse, afectando búsquedas futuras de módulos y subpaquetes
contenidos en el paquete.

Aunque esta característica no se necesita frecuentemente, puede usarse para
extender el conjunto de módulos que se encuentran en el paquete.


.. rubric:: Footnotes

.. [#] De hecho las definiciones de función son también 'declaraciones' que
   se 'ejecutan';  la ejecución mete el nombre de la función en el espacio
   de nombres global.
