.. _tut-morecontrol:

*************************************
Más herramientas para Control de Flujo
*************************************

Además de la sentencia :keyword:`while` que acabamos de introducir,
Python entiende las sentencias de control de flujo que podemos encontrar en otros
lenguajes, con algunos cambios.


.. _tut-if:

La Sentencia :keyword:`if` 
===============

Tal vez el tipo más conocido de sentencias sea la sentencia :keyword:`if`.  Por
ejemplo::

   >>> x = int(raw_input("Please enter an integer: "))
   >>> if x < 0:
   ...      x = 0
   ...      print 'Negative changed to zero'
   ... elif x == 0:
   ...      print 'Zero'
   ... elif x == 1:
   ...      print 'Single'
   ... else:
   ...      print 'More'
   ... 

Puede haber cero o más bloques :keyword:`elif`, y el bloque :keyword:`else` es 
opcional. La palabra reservada ':keyword:`elif`' es una abreviación de 'else if', y es
útil para evitar identación excesiva. Una sequencia :keyword:`if` ... :keyword:`elif` ...
:keyword:`elif` ... sustituye las sentencias ``switch`` o ``case`` encontradas en otros
lenguajes.


.. _tut-for:

La Sentencia :keyword:`for`
================

.. index::
   statement: for
   statement: for

La sentencia :keyword:`for` en Python difiere un poco de lo que uno puede estar
acostumbrado en lenguajes como C o Pascal. En lugar de siempre iterar sobre una
progresión aritmética de números (como en Pascal) o darle al usuario la posibilidad de
definir tanto el paso de la iteración y condición de fin (como en C), la sentencia 
:keyword:`for` de Python itera sobre los items de cualquier sequencia (una lista
o una cadena de texto), en el orden que aparcen en la secuencia. Por ejemplo
(no pun intended):

.. One suggestion was to give a real C example here, but that may only serve to
   confuse non-C programmers.

::

   >>> # Measure some strings:
   ... a = ['cat', 'window', 'defenestrate']
   >>> for x in a:
   ...     print x, len(x)
   ... 
   cat 3
   window 6
   defenestrate 12

No es seguro modificar la secuencia sobre la que se está iterando en el loop (esto solo
es posible para tipos de secuencias mutables, como las listas). Si se necesita modificar
la lista sobre la que se está iterando (por ejemplo, para duplicar items seleccionados)
se debe iterar sobre una copia. La notación de rebanada es conveniente para esto::

   >>> for x in a[:]: # make a slice copy of the entire list
   ...    if len(x) > 6: a.insert(0, x)
   ... 
   >>> a
   ['defenestrate', 'cat', 'window', 'defenestrate']


.. _tut-range:

La Función :func:`range`
==============

Si se necesita iterar sobre una secuencia de números, es apropiado utilizar
la función incorporada :func:`range`.  Genera una lista conteniendo progresiones
aritméticas::

   >>> range(10)
   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

El valor final dado nunca esparte de la lista; ``range(10)`` genera una lista de 10
valores, los índices correspondientes para los items de una secuencia de longitud 10.
Es posible hacer que el rango empiece con otro número, o especificar un incremento
diferente (incluso negativos; algunas veces se lo llama 'paso')::

   >>> range(5, 10)
   [5, 6, 7, 8, 9]
   >>> range(0, 10, 3)
   [0, 3, 6, 9]
   >>> range(-10, -100, -30)
   [-10, -40, -70]

Para iterar sobre los índices de una secuencia, se combina :func:`range` y :func:`len`
así::

   >>> a = ['Mary', 'had', 'a', 'little', 'lamb']
   >>> for i in range(len(a)):
   ...     print i, a[i]
   ... 
   0 Mary
   1 had
   2 a
   3 little
   4 lamb


.. _tut-break:

Las Sentencias :keyword:`break` y :keyword:`continue`, y la Clausula :keyword:`else` en Loops
=========================================================================================

La sentencia :keyword:`break`, como en C, termina el loop :keyword:`for` o 
:keyword:`while` más anidado.

La sentencia :keyword:`continue`, también tomada prestada de C, continua
con la próxima iteración del loop.

Las setencias de loop pueden tener una clausula ``else``; es ejecutada cuando
el loop termina luego de agotar la lista (con :keyword:`for`) o cuando la condición
se hace falsa (con :keyword:`while`), pero no cuando el loop es terminado
con la sentencia :keyword:`break`. Se ejemplifica en el siguiente loop, que busca
números primos::

   >>> for n in range(2, 10):
   ...     for x in range(2, n):
   ...         if n % x == 0:
   ...             print n, 'equals', x, '*', n/x
   ...             break
   ...     else:
   ...         # loop fell through without finding a factor
   ...         print n, 'is a prime number'
   ... 
   2 is a prime number
   3 is a prime number
   4 equals 2 * 2
   5 is a prime number
   6 equals 2 * 3
   7 is a prime number
   8 equals 2 * 4
   9 equals 3 * 3


.. _tut-pass:

La Sentencia :keyword:`pass` 
==================

La sentencia :keyword:`pass` no hace nada. Se puede usar cuando una sentencia
es requerida por la sintáxis pero el programa no requiere ninguna acción. 
Por ejemplo::

   >>> while True:
   ...       pass # Busy-wait for keyboard interrupt
   ... 


.. _tut-functions:

Definiendo funciones
=============

Podemos crear una función que escriba la serie de Fibonacci hasta una límite
determinado::

   >>> def fib(n):    # write Fibonacci series up to n
   ...     """Print a Fibonacci series up to n."""
   ...     a, b = 0, 1
   ...     while b < n:
   ...         print b,
   ...         a, b = b, a+b
   ... 
   >>> # Now call the function we just defined:
   ... fib(2000)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597

.. index::
   single: documentation strings
   single: docstrings
   single: strings, documentation

La palabra reservada :keyword:`def` de una para *definir* funciones.  Debe seguirle
el nombre de la función y la lista de parámetros formales entre paréntesis. Las 
sentencias que forman el cuerpo de la función empiezan en la linea siguiente, y deben
estar identadas. La primer sentencia del cuerpo de la función puede ser opcionalmente
una cadena de texto litaral; esta es la cadena de texto de documentación de la 
función, o :dfn:`docstring`.

Hay herramientas que usan las docstrings para producir automáticamente 
documentación en líne o imprimible, o para permitirle al usuario que navegue el
código en forma interactiva; es una buena práctica incluir docstrings enel código
que uno escriba, así que se debe intentar hacer un hábito de esto.

La *ejecución* de una función introduce una nueva tabla de símbolos usada para las
variables locales de la función. Más precisamente, todas las asignaciones de variables
en la función almacenan el valor en la tabla de símbolos local; así mismo la referencia
a variables primero mira la tabla de símbolos local, luego en la tabla de símbolos local
de las funciones externas, luego la tabla de sínbolos global, y finalmente la tabla de
nombres predefinidos. Así, no se les puede asignar directamente un valor a las
variables globales dentro de una función (a menos se las nombre en la sentencia
:keyword:`global`), aunque si pueden ser referenciadas.

Los parámetros reales (arguementos) de una función se introducen
en la tabla de símbolos local de la función llamada cuando esta es llamada; así, los
argumentos son pasados *por valor* (dónde el *valor* es siempre una *referencia*
a un objeto, no el valor del objeto). [#]_ Cuando una función llama a otra función,
una nueva tabla de símbolos local es creada para esa llamada.

La definición de una función introduce el nombre de la función en la tabla de
símbolos actual. El valor del nombre de la función tiene un tipo que es reconocido
por el interprete como una función definida por el usuario. Este valor puede ser 
asignado a otro nombre que luego puede ser usado ocmo una función. Esto sirve como
un mecanismo general para renombrar::

   >>> fib
   <function fib at 10042ed0>
   >>> f = fib
   >>> f(100)
   1 1 2 3 5 8 13 21 34 55 89

Se puede objetar que ``fib`` no es una función, sino un procedimiento. En Python,
como en C, los procedimientos son solo funciones que no retornan un valor. De hecho,
tecnicamente hablando, los procedimientos si retornan un valor, aunque uno aburrido.
Este valor es llamada ``None`` (es un nombre predefinido).  El intérprete por lo 
general no escribe el valor ``None`` si va a ser el único valor escrito. Si realmente
se quiere, se puede verlo usando :keyword:`print`::

   >>> fib(0)
   >>> print fib(0)
   None

Es simple escribir una función que retorne una lista con los números de la serie de 
Fibonacci en lugar de imprimirlos::

   >>> def fib2(n): # return Fibonacci series up to n
   ...     """Return a list containing the Fibonacci series up to n."""
   ...     result = []
   ...     a, b = 0, 1
   ...     while b < n:
   ...         result.append(b)    # see below
   ...         a, b = b, a+b
   ...     return result
   ... 
   >>> f100 = fib2(100)    # call it
   >>> f100                # write the result
   [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

Este ejemplo, como es usual, demuestra algunas características más de Python:

* La sentencia :keyword:`return` devuelve un valor en una función.
  :keyword:`return` sin una expresión como argumento retorna ``None``. Si se
  alcanza el final de un procedimiento, también se retorna ``None``.

* La sentencia ``result.append(b)`` llama al *método* del objeto lista ``result``.  
  Un método es una función que 'pertenece' a unobjeto y se nombra 
  ``obj.methodname``, dónde ``obj`` es algún objeto (puede ser una expresión),
  y ``methodname`` es el nombre del método que está definido por el tipo del objeto.
  Distintos tipos definen distintos métodos. Métodos de diferentes tipos pueden tener 
  el mismo nombre sin causar ambiguedad. (Es posible definir tipos de objetos propios,
  y métodos, usando *clases*, como se discutirá más adelante en el tutorial).
  El método :meth:`append` mostrado en el ejemplo está definidio para objetos lista;
  añade un nuevo elemento al final de la lista. En este ejemplo es equivalente a
  adds a new element at the end of the list.  In this example it is equivalent to
  ``result = result + [b]``, pero más eficiente.


.. _tut-defining:

Más sobre Definición de Funciones
==========================

También es posible definir funciones with un número variable de argumentos. Hay
tres formas que pueden ser combinadas.


.. _tut-defaultargs:

Argumentos con Valores por Defecto
-------------------------------------------------

La forma más útil es especificar un valor por defecto para  uno o más argumentos.
Esto crea una función que puede ser llamada con menos argumentos que los que
permite. Por ejemplo::

   def ask_ok(prompt, retries=4, complaint='Yes or no, please!'):
       while True:
           ok = raw_input(prompt)
           if ok in ('y', 'ye', 'yes'): return True
           if ok in ('n', 'no', 'nop', 'nope'): return False
           retries = retries - 1
           if retries < 0: raise IOError, 'refusenik user'
           print complaint

Esta función puede ser llamada tanto así: ``ask_ok('Do you really want to
quit?')`` como así: ``ask_ok('OK to overwrite the file?', 2)``.

Este ejemplo también introduce la palabra reservada :keyword:`in`. Prueba si una 
secuencia contiene o no un determinado valor.

Los valores por defecto son evaluados en el momento de la definición de la función, en
el ámbito de *definición*, entonces::

   i = 5

   def f(arg=i):
       print arg

   i = 6
   f()

imprimirá ``5``.

**Advertencia importante:**  El valor por defecto es evaluado solo una vez. Existe una
diferencia cuando el valor por defecto es un objeto mutable como una lista, diccionario,
o instancia de la mayoría de las calses. Por ejemplo, la siguiente función acumula los 
argumentos que se le pasan en sbusiguientes llamadas::

   def f(a, L=[]):
       L.append(a)
       return L

   print f(1)
   print f(2)
   print f(3)

Imprimirá::

   [1]
   [1, 2]
   [1, 2, 3]

Si no se quiere que el valor por defecto sea compartido entre subsiguientes llamdas,
se pueden escribir la función así::

   def f(a, L=None):
       if L is None:
           L = []
       L.append(a)
       return L


.. _tut-keywordargs:

Palabras Claves como Argumentos
---------------------------------------------

Las funciones también puede ser llamadas usando palabras claves como argumentos
de la forma ``keyword = value``.  Por ejemplo, la siguiente función::

   def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
       print "-- This parrot wouldn't", action,
       print "if you put", voltage, "volts through it."
       print "-- Lovely plumage, the", type
       print "-- It's", state, "!"

puede ser llamada de cualquiera de las siguientes formas::

   parrot(1000)
   parrot(action = 'VOOOOOM', voltage = 1000000)
   parrot('a thousand', state = 'pushing up the daisies')
   parrot('a million', 'bereft of life', 'jump')

pero estas otras llamadas serían todas inválidas::

   parrot()                     # required argument missing
   parrot(voltage=5.0, 'dead')  # non-keyword argument following keyword
   parrot(110, voltage=220)     # duplicate value for argument
   parrot(actor='John Cleese')  # unknown keyword

En general, una lista de argumentos debe tener todos sus argumentos posicionales
seguidos por los argumentos de palabra clave, dónde las palabras claves deben ser
elegidas entre los nombres de los parámetros formales. No es importante si un 
parámetro formal tiene un valor por defecto o no. Ningún argumento puede recibir
un valor más de una vez (los nombres de parámetros formales correspondientes a 
argumentos posicionales no pueden ser usados como palabras clave en la misma
llamada. Aquí hay un ejemplo que falla debido a esta restricción::

   >>> def function(a):
   ...     pass
   ... 
   >>> function(0, a=0)
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: function() got multiple values for keyword argument 'a'

Cuando un parámetro formal de la forma ``**name`` está presente al final, recive
un diccionario (ver :ref:`typesmapping`) conteniendo todos los argumentos de palabras
clave excepto aquellos correspondientes a un parámetro formal. Esto puede ser 
combinado con un parámetro formal de la forma ``*name`` (descripto en la siguiente
subsección) que recibe una tupla conteniendo los argumentos pocicionales además de
lalista de parámetros formales. (``*name`` debe ocurrir antes de ``**name``).
Por ejemplo, si definimos una función así::

   def cheeseshop(kind, *arguments, **keywords):
       print "-- Do you have any", kind, '?'
       print "-- I'm sorry, we're all out of", kind
       for arg in arguments: print arg
       print '-'*40
       keys = keywords.keys()
       keys.sort()
       for kw in keys: print kw, ':', keywords[kw]

Puede ser llamada así::

   cheeseshop('Limburger', "It's very runny, sir.",
              "It's really very, VERY runny, sir.",
              client='John Cleese',
              shopkeeper='Michael Palin',
              sketch='Cheese Shop Sketch')

y por supuesto imprimirá::

   -- Do you have any Limburger ?
   -- I'm sorry, we're all out of Limburger
   It's very runny, sir.
   It's really very, VERY runny, sir.
   ----------------------------------------
   client : John Cleese
   shopkeeper : Michael Palin
   sketch : Cheese Shop Sketch

Se debe notar que el método :meth:`sort` de la lista de nombres de argumentos 
de palabra clave es llamado antes de imprimir el contenido del diccionario 
``keywords``; si esto no se hace, el orden en que los argumentos son impresos
no está definido.

.. _tut-arbitraryargs:

Listas de Argumentos Arbritrarios
--------------------------------------------

.. index::
  statement: *  

Finalmente, la opción menos frecuentemente usada es especificar que una función
puede ser llamada con un número arbitrario de argumentos.  Estos argumentos serán
organizados en una tupla. Antes del número variable de argumentos, cero o más 
argumentos normales pueden estar presentes.::

   def fprintf(file, template, *args):
       file.write(template.format(args))


.. _tut-unpacking-arguments:

Desempaquetando una Lista de Argumentos
----------------------------------------------------------

La situación inversaa ocurre cuando los argumentos ya están en una lista o tupla
pero necesitan sen desempaquetados para llamar a una función que requiere 
argumentos posicionales separados. Por ejemplo, la función predefinida :func:`range` 
espera los argumentos *inicio* y *fin*.  Si no están disponibles en forma separada,
se puede escribir la llamada a la función con el operador para desempaquetar 
argumentos de una lista o una tupla ``*``\::

   >>> range(3, 6)             # normal call with separate arguments
   [3, 4, 5]
   >>> args = [3, 6]
   >>> range(*args)            # call with arguments unpacked from a list
   [3, 4, 5]

.. index::
  statement: **

Del mismo modo, los diccionarios pueden entregar argumentos de palabra clave con el 
operador ``**``\::

   >>> def parrot(voltage, state='a stiff', action='voom'):
   ...     print "-- This parrot wouldn't", action,
   ...     print "if you put", voltage, "volts through it.",
   ...     print "E's", state, "!"
   ...
   >>> d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
   >>> parrot(**d)
   -- This parrot wouldn't VOOM if you put four million volts through it. E's bleedin' demised !


.. _tut-lambda:

Lambda Forms
------------

By popular demand, a few features commonly found in functional programming
languages like Lisp have been added to Python.  With the :keyword:`lambda`
keyword, small anonymous functions can be created. Here's a function that
returns the sum of its two arguments: ``lambda a, b: a+b``.  Lambda forms can be
used wherever function objects are required.  They are syntactically restricted
to a single expression.  Semantically, they are just syntactic sugar for a
normal function definition.  Like nested function definitions, lambda forms can
reference variables from the containing scope::

   >>> def make_incrementor(n):
   ...     return lambda x: x + n
   ...
   >>> f = make_incrementor(42)
   >>> f(0)
   42
   >>> f(1)
   43


.. _tut-docstrings:

Documentation Strings
---------------------

.. index::
   single: docstrings
   single: documentation strings
   single: strings, documentation

There are emerging conventions about the content and formatting of documentation
strings.

The first line should always be a short, concise summary of the object's
purpose.  For brevity, it should not explicitly state the object's name or type,
since these are available by other means (except if the name happens to be a
verb describing a function's operation).  This line should begin with a capital
letter and end with a period.

If there are more lines in the documentation string, the second line should be
blank, visually separating the summary from the rest of the description.  The
following lines should be one or more paragraphs describing the object's calling
conventions, its side effects, etc.

The Python parser does not strip indentation from multi-line string literals in
Python, so tools that process documentation have to strip indentation if
desired.  This is done using the following convention. The first non-blank line
*after* the first line of the string determines the amount of indentation for
the entire documentation string.  (We can't use the first line since it is
generally adjacent to the string's opening quotes so its indentation is not
apparent in the string literal.)  Whitespace "equivalent" to this indentation is
then stripped from the start of all lines of the string.  Lines that are
indented less should not occur, but if they occur all their leading whitespace
should be stripped.  Equivalence of whitespace should be tested after expansion
of tabs (to 8 spaces, normally).

Here is an example of a multi-line docstring::

   >>> def my_function():
   ...     """Do nothing, but document it.
   ... 
   ...     No, really, it doesn't do anything.
   ...     """
   ...     pass
   ... 
   >>> print my_function.__doc__
   Do nothing, but document it.

       No, really, it doesn't do anything.


.. _tut-codingstyle:

Intermezzo: Coding Style
========================

.. sectionauthor:: Georg Brandl <georg@python.org>
.. index:: pair: coding; style

Now that you are about to write longer, more complex pieces of Python, it is a
good time to talk about *coding style*.  Most languages can be written (or more
concise, *formatted*) in different styles; some are more readable than others.
Making it easy for others to read your code is always a good idea, and adopting
a nice coding style helps tremendously for that.

For Python, :pep:`8` has emerged as the style guide that most projects adhere to;
it promotes a very readable and eye-pleasing coding style.  Every Python
developer should read it at some point; here are the most important points
extracted for you:

* Use 4-space indentation, and no tabs.

  4 spaces are a good compromise between small indentation (allows greater
  nesting depth) and large indentation (easier to read).  Tabs introduce
  confusion, and are best left out.

* Wrap lines so that they don't exceed 79 characters.

  This helps users with small displays and makes it possible to have several
  code files side-by-side on larger displays.

* Use blank lines to separate functions and classes, and larger blocks of
  code inside functions.

* When possible, put comments on a line of their own.

* Use docstrings.

* Use spaces around operators and after commas, but not directly inside
  bracketing constructs: ``a = f(1, 2) + g(3, 4)``.

* Name your classes and functions consistently; the convention is to use
  ``CamelCase`` for classes and ``lower_case_with_underscores`` for functions
  and methods.  Always use ``self`` as the name for the first method argument.

* Don't use fancy encodings if your code is meant to be used in international
  environments.  Plain ASCII works best in any case.


.. rubric:: Footnotes

.. [#] Actually, *call by object reference* would be a better description,
   since if a mutable object is passed, the caller will see any changes the
   callee makes to it (items inserted into a list).

