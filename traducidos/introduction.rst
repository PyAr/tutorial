.. _tut-informal:

**********************************
Una Introducción Informal a Python
**********************************

En los siguientes ejemplos, las entradas y salidas son distinguidas por la
presencia o ausencia de los prompts (```>>>``` and ```...```): para
reproducir los ejemplos, debes escribir todo lo que esté después del prompt,
cuando este aparezca; las líneas que no comiencen con el prompt son las
salidas del intérprete. Tenga en cuenta que el prompt secundario que
aparece por sí sólo en una línea de un ejemplo significa que debe escribir
una línea en blanco; esto es usado para terminar un comando multilínea.

Muchos de los ejemplos de este manual, incluso aquellos ingresados en el prompt
interactivo, incluyen comentarios. Los comentarios en Python comienzan con
el caracter numeral, ``#``, y se extienden hasta el final físico de la
línea. Un comentario quizás aparezca al comiendo de la línea o seguidos
de espacios blancos o código, pero sin una cadena de caracteres.
Un caracter numeral dentro de una cadena de caracteres es sólo un caracter
numeral.

Algunos ejemplos::

   # este es el primer comentario
   SPAM = 1                 # y este es el segundo comentario
                            # ... y ahora un tercero!
   STRING = "# Este no es un comentario".


.. _tut-calculator:

Usar Python como una Calculadora
================================

Vamos a probar algunos comandos simples en Python. Inicia un intérprete y
espera por el prompt primario, ``>>>``. (No debería demorar tanto).

.. _tut-numbers:

Números
-------

El intérprete actúa como una simple calculadora; puedes tipear una expresión
y este escribirá los valores. La sintaxis es sencilla: los operadores ``+``, ``-``,
``*`` y ``/`` funcionan como en la mayoría de los lenguajes (por ejemplo,
Pascal o C); los paréntesis pueden ser usados para agrupar. Por ejemplo::

   >>> 2+2
   4
   >>> # Este es un comentario
   ... 2+2
   4
   >>> 2+2  # y un comentario en la misma línea que el código
   4
   >>> (50-5*6)/4
   5
   >>> # La división entera retorna el piso:
   ... 7/3
   2
   >>> 7/-3
   -3

El signo igual (``=``) es usado para asignar un valor a una variable. Luego,
ningún resultado es mostrado antes del próximo prompt::

   >>> width = 20
   >>> height = 5*9
   >>> width * height
   900

Un valor puede ser asignado a varias variables simultáneamente::

   >>> x = y = z = 0  # Zero x, y and z
   >>> x
   0
   >>> y
   0
   >>> z
   0

Los números de punto flotante tiene soporte completo; las operaciones con
mezclas en los tipos de los operandos convierte los enteros a punto flotante::

   >>> 3 * 3.75 / 1.5
   7.5
   >>> 7.0 / 2
   3.5

Los números complejos también están soportados; los números imaginarios son
escritos con el sufijo de ``j`` o ``J``. Los números complejos con un
componente real que no sea cero son escritos como ``(real+imagj)``, o pueden
ser escrito con la función ``complex(real, imag)``.
::

   >>> 1j * 1J
   (-1+0j)
   >>> 1j * complex(0,1)
   (-1+0j)
   >>> 3+1j*3
   (3+3j)
   >>> (3+1j)*3
   (9+3j)
   >>> (1+2j)/(1+1j)
   (1.5+0.5j)

Los números complejos son siempre representados como dos números de punto
flotante, la parte real y la imaginaria. Para extraer estas partes desde un
número complejo *z*, usa ``z.real`` y ``z.imag``. ::

   >>> a=1.5+0.5j
   >>> a.real
   1.5
   >>> a.imag
   0.5

La función de conversión de los punto flotante y enteros (:func:`float`,
:func:`int` y :func:`long`) no funciona para números complejos --- aquí no hay
una forma correcta de convertir un número complejo a un número real. Usa
``abs(z)`` para obtener esta magnitud (como un flotante) o ``z.real`` para
obtener la parte real. ::

   >>> a=3.0+4.0j
   >>> float(a)
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: can't convert complex to float; use abs(z)
   >>> a.real
   3.0
   >>> a.imag
   4.0
   >>> abs(a)  # sqrt(a.real**2 + a.imag**2)
   5.0
   >>>

En el modo interactivo, la última expresion impresa es asignada a la variable
``_``. Esto significa que cuando estés usando Python como una calculadora de
escritorio, es más fácil seguir calculando, por ejemplo::

   >>> tax = 12.5 / 100
   >>> price = 100.50
   >>> price * tax
   12.5625
   >>> price + _
   113.0625
   >>> round(_, 2)
   113.06
   >>>

Esta variable debería ser tratada como de sólo lectura por el usuario. No
asignes explícitamente un valor a esta --- crearás una variable local
independiente con el mismo nombre enmascarando la variable incorporada con el
comportamiento mágico.

.. _tut-strings:

Cadenas de caracteres
---------------------

Además de números, Python puede manipular cadenas de texto, las cuales pueden
ser expresadas de distintas formas. Pueden ser encerradas en comillas simples
o dobles::

   >>> 'huevos y pan'
   'huevos y pan'
   >>> 'doesn\'t'
   "doesn't"
   >>> "doesn't"
   "doesn't"
   >>> '"Si," le dijo.'
   '"Si," le dijo.'
   >>> "\"Si,\" le dijo."
   '"Si," le dijo.'
   >>> '"Isn\'t," she said.'
   '"Isn\'t," she said.'

Las cadenas de texto literales pueden contener múltiples líneas de distintas
formas. String literals can span multiple lines in several ways.  Las
líneas continuas se pueden usar, con una barra invertida como el último
caracter de la línea para indicar que la siguiente línea es la continuación
lógica de la línea::

   hola = "Esta es una larga cadena que contiene\n\
   varias líneas de texto, tal y como se hace en C.\n\
       Notar que los espacios en blanco al principio de la linea\
    son significantes."

   print hola

Notá que de todas formas se necesita embeber los salto de líneas con ``\n``;
la nueva línea que sigue a la barra invertida final es descartada. Este ejemplo
imprimiría::

   Esta es una larga cadena que contiene
   varias líneas de texto, tal y como se hace en C.
        Notar que los espacios en blanco al principio de la linea son
        significantes.

Si se hace de la cadena de texto una cadena "cruda", la secuencia ``\n`` no
es convertida a salto de línea, pero la barra invertida al final de la línea
y el caracter de nueva línea en la fuente, ambos son incluidos en la cadena
como datos. Asi, el ejemplo::

   hola = r"Esta es una larga cadena que contiene\n\
   varias líneas de texto, tal y como se hace en C."

   print hello

imprimirá::

   Esta es una larga cadena que contiene\n\
   varias líneas de texto, tal y como se hace en C.

O, las cadenas de texto pueden er rodeadas en un par de comillas triples:
``"""`` o ``'''``.  No se necesita escapar los finales de línea cuando se 
utilizan comillas triples, pero serán incluídos en la cadena. ::

   print """
   Uso: algo [OPTIONS]
        -h                        Muestra el mensaje de uso
        -H nombrehost             Nombre del host al cual conectarse
   """

produce la siguiente salida::

   Uso: algo [OPTIONS]
        -h                        Muestra el mensaje de uso
        -H nombrehost             Nombre del host al cual conectarse

El interprete imprime el resultado de operaciones entre cadenas de la misma
forma en que son tipeadas como entrada: dentro de comillas, y con comillas y
otros caracteres graciosos escapados con barras invertidas, para mostrar
el valor preciso. La cadena de texto es encerrada en comillas dobles si
contiene una comilla simple y no comillas dobles, sino es encerrada en comillas
simples. (La declaración :keyword:`print`, descripta luego,
puede ser usado para escribir cadenas sin comillas o escapes).

Las cadenas de texto pueden ser concatenadas (pegadas juntas) con el operador
``+`` y repetidas con ``*``::

   >>> palabra = 'Ayuda' + 'A'
   >>> palabra
   'AyudaA'
   >>> '<' + palabra*5 + '>'
   '<AyudaAAyudaAAyudaAAyudaAAyudaA>'

Dos cadenas de texto juntas son automáticamente concatenadas; la primer línea
del ejemplo anterior podría haber sido escrita ``word = 'Help' 'A'``; esto
solo funciona con dos literales, no con expresiones arbitrarias::

   >>> 'cad' 'ena'                   #  <-  Esto es correcto
   'cadena'
   >>> 'cad'.strip() + 'ena'   #  <-  Esto es correcto
   'cadena'
   >>> 'cad'.strip() 'ena'     #  <-  Esto no es correcto
     File "<stdin>", line 1, in ?
       'cad'.strip() 'ena'
                         ^
   SyntaxError: invalid syntax

Las cadenas de texto se pueden indexar; comoen C, el primer caracter de la
cadena tiene el índice 0. No hay un tipo de dato para los caracteres; un
caracter is simplemente una cadena de longitud uno. Como en Icon, se pueden
especificar sub cadenas con la *notación de rebanadas*: dos índices separados
por dos puntos. ::

   >>> palabra[4]
   'a'
   >>> palabra[0:2]
   'Ay'
   >>> palabra[2:4]
   'ud'

Los índices de las rebanadas tienen valores por defecto útiles; el valor por
defecto para el primer índice es cero, el valor por defecto para el segundo
índice es la longitud de la cadena a rebanar. ::

   >>> palabra[:2]    # Los primeros dos caracteres
   'Ay'
   >>> palabra[2:]    # Todo menos los primeros dos caracteres
   'udaA'

A diferencia de las cadenas de texto en C, en Python no pueden ser cambiadas.
Intentar asignar a una posición indexada da un error::

   >>> palabra[0] = 'x'
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: object doesn't support item assignment
   >>> palabra[:1] = 'Mas'
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: object doesn't support slice assignment

Sin embarjo, crear una nueva cadena con contenido combinado es fácil y
eficiente::

   >>> 'x' + palabra[1:]
   'xyudaA'
   >>> 'Mas' + palabra[5]
   'MasA'

Aquí algo útil de las operaciones de rebanada: ``s[:i] + s[i:]`` es ``s``.
::

   >>> palabra[:2] + palabra[2:]
   'AyudaA'
   >>> palabra[:3] + palabra[3:]
   'AyudaA'

Índices degenerados en las rebanadas son manejados con mucha gracia: un índice
muy largo es reemplazado por la longitud de la cadena, un límite superior más
chico que el límite menor retorna una cadena vacía. ::

   >>> palabra[1:100]
   'yudaA'
   >>> palabra[10:]
   ''
   >>> palabra[2:1]
   ''

Los índices pueden ser números negativos, para empezar a contar desde la
derecha. Por ejemplo::

   >>> palabra[-1]     # El ultimo caracter
   'A'
   >>> palabra[-2]     # El penultimo caracter
   'a'
   >>> palabra[-2:]    # Los últimos dos caracteres
   'aA'
   >>> word[:-2]    # Todo menos los últimos dos caracteres
   'Ayud'

Pero notá que -0 es en realidad lo mismo que 0, ¡por lo que no cuenta desde
la derecha!
::

   >>> palabra[-0]     # (ya que -0 es igual a 0)
   'A'

Los índices negativos fuera de rango son truncados, pero esto no anda para
índices de un solo elemento (no rebanada)::

   >>> palabra[-100:]
   'AyudaA'
   >>> palabra[-10]    # error
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   IndexError: string index out of range

Una forma de recordar cómo funcionan las rebanadas es pensar en los índices
como puntos *entre* caracteres, con el punto a la izquierda del primer caracter
numerado en 0. Luego, el punto a la derecha del último caracter de una cadena
de *n* caracteres tienen índice *n*, por ejemplo::

    +---+---+---+---+---+---+
    | A | y | u | d | a | A |
    +---+---+---+---+---+---+
    0   1   2   3   4   5   6
   -6  -5  -4  -3  -2  -1

La primer fila de números da la posición de los índices 0...6 en la cadena;
la segunda fila da los correspondientes índices negativos. La rebanada de *i*
a *j* consiste en todos los caracters entre los puntos etiquetados *i* y *j*,
respectivamente.

Para índices no negativos, la longitud de la rebanada es la diferencia de los
índices, si ambos entran en los límites. Por ejemplo, la longitud de
``palabra[1:3]`` es 2.

La función incorporada :func:`len` devuelve la longitud de una cadena
de texto::

   >>> s = 'supercalifrastilisticoespialidoso'
   >>> len(s)
   33


.. seealso::

   :ref:`typesseq`
      Las cadenas de texto y la cadenas de texto Unicode descriptas en la
      siguiente sección, son ejemplos de *tipos secuencias*, y soportan
      las operaciones comunes para esos tipos.

   :ref:`string-methods`
      Tanto las cadenas de texto como las cadenas de texto Unicode soportan
      una gran cantidad de métodos para tranformaciones básicas y búsqueda.

   :ref:`new-string-formatting`
      Aquí se da información sobre fromateo de cadenas de texto con
      :meth:`str.format`.

   :ref:`string-formatting`
      Aquí se describe con más detalle las operaciones viejas para formateo
      usadas cuando una cadena de texto o una cadena Unicode están a la
      izquierda del operador ``%``.


.. _tut-unicodestrings:

Unicode Strings
---------------

.. sectionauthor:: Marc-Andre Lemburg <mal@lemburg.com>


Starting with Python 2.0 a new data type for storing text data is available to
the programmer: the Unicode object. It can be used to store and manipulate
Unicode data (see http://www.unicode.org/) and integrates well with the existing
string objects, providing auto-conversions where necessary.

Unicode has the advantage of providing one ordinal for every character in every
script used in modern and ancient texts. Previously, there were only 256
possible ordinals for script characters. Texts were typically bound to a code
page which mapped the ordinals to script characters. This lead to very much
confusion especially with respect to internationalization (usually written as
``i18n`` --- ``'i'`` + 18 characters + ``'n'``) of software.  Unicode solves
these problems by defining one code page for all scripts.

Creating Unicode strings in Python is just as simple as creating normal
strings::

   >>> u'Hello World !'
   u'Hello World !'

The small ``'u'`` in front of the quote indicates that a Unicode string is
supposed to be created. If you want to include special characters in the string,
you can do so by using the Python *Unicode-Escape* encoding. The following
example shows how::

   >>> u'Hello\u0020World !'
   u'Hello World !'

The escape sequence ``\u0020`` indicates to insert the Unicode character with
the ordinal value 0x0020 (the space character) at the given position.

Other characters are interpreted by using their respective ordinal values
directly as Unicode ordinals.  If you have literal strings in the standard
Latin-1 encoding that is used in many Western countries, you will find it
convenient that the lower 256 characters of Unicode are the same as the 256
characters of Latin-1.

For experts, there is also a raw mode just like the one for normal strings. You
have to prefix the opening quote with 'ur' to have Python use the
*Raw-Unicode-Escape* encoding. It will only apply the above ``\uXXXX``
conversion if there is an uneven number of backslashes in front of the small
'u'. ::

   >>> ur'Hello\u0020World !'
   u'Hello World !'
   >>> ur'Hello\\u0020World !'
   u'Hello\\\\u0020World !'

The raw mode is most useful when you have to enter lots of backslashes, as can
be necessary in regular expressions.

Apart from these standard encodings, Python provides a whole set of other ways
of creating Unicode strings on the basis of a known encoding.

.. index:: builtin: unicode

The built-in function :func:`unicode` provides access to all registered Unicode
codecs (COders and DECoders). Some of the more well known encodings which these
codecs can convert are *Latin-1*, *ASCII*, *UTF-8*, and *UTF-16*. The latter two
are variable-length encodings that store each Unicode character in one or more
bytes. The default encoding is normally set to ASCII, which passes through
characters in the range 0 to 127 and rejects any other characters with an error.
When a Unicode string is printed, written to a file, or converted with
:func:`str`, conversion takes place using this default encoding. ::

   >>> u"abc"
   u'abc'
   >>> str(u"abc")
   'abc'
   >>> u"äöü"
   u'\xe4\xf6\xfc'
   >>> str(u"äöü")
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-2: ordinal not in range(128)

To convert a Unicode string into an 8-bit string using a specific encoding,
Unicode objects provide an :func:`encode` method that takes one argument, the
name of the encoding.  Lowercase names for encodings are preferred. ::

   >>> u"äöü".encode('utf-8')
   '\xc3\xa4\xc3\xb6\xc3\xbc'

If you have data in a specific encoding and want to produce a corresponding
Unicode string from it, you can use the :func:`unicode` function with the
encoding name as the second argument. ::

   >>> unicode('\xc3\xa4\xc3\xb6\xc3\xbc', 'utf-8')
   u'\xe4\xf6\xfc'


.. _tut-lists:

Lists
-----

Python knows a number of *compound* data types, used to group together other
values.  The most versatile is the *list*, which can be written as a list of
comma-separated values (items) between square brackets.  List items need not all
have the same type. ::

   >>> a = ['spam', 'eggs', 100, 1234]
   >>> a
   ['spam', 'eggs', 100, 1234]

Like string indices, list indices start at 0, and lists can be sliced,
concatenated and so on::

   >>> a[0]
   'spam'
   >>> a[3]
   1234
   >>> a[-2]
   100
   >>> a[1:-1]
   ['eggs', 100]
   >>> a[:2] + ['bacon', 2*2]
   ['spam', 'eggs', 'bacon', 4]
   >>> 3*a[:3] + ['Boo!']
   ['spam', 'eggs', 100, 'spam', 'eggs', 100, 'spam', 'eggs', 100, 'Boo!']

Unlike strings, which are *immutable*, it is possible to change individual
elements of a list::

   >>> a
   ['spam', 'eggs', 100, 1234]
   >>> a[2] = a[2] + 23
   >>> a
   ['spam', 'eggs', 123, 1234]

Assignment to slices is also possible, and this can even change the size of the
list or clear it entirely::

   >>> # Replace some items:
   ... a[0:2] = [1, 12]
   >>> a
   [1, 12, 123, 1234]
   >>> # Remove some:
   ... a[0:2] = []
   >>> a
   [123, 1234]
   >>> # Insert some:
   ... a[1:1] = ['bletch', 'xyzzy']
   >>> a
   [123, 'bletch', 'xyzzy', 1234]
   >>> # Insert (a copy of) itself at the beginning
   >>> a[:0] = a
   >>> a
   [123, 'bletch', 'xyzzy', 1234, 123, 'bletch', 'xyzzy', 1234]
   >>> # Clear the list: replace all items with an empty list
   >>> a[:] = []
   >>> a
   []

The built-in function :func:`len` also applies to lists::

   >>> a = ['a', 'b', 'c', 'd']
   >>> len(a)
   4

It is possible to nest lists (create lists containing other lists), for
example::

   >>> q = [2, 3]
   >>> p = [1, q, 4]
   >>> len(p)
   3
   >>> p[1]
   [2, 3]
   >>> p[1][0]
   2
   >>> p[1].append('xtra')     # See section 5.1
   >>> p
   [1, [2, 3, 'xtra'], 4]
   >>> q
   [2, 3, 'xtra']

Note that in the last example, ``p[1]`` and ``q`` really refer to the same
object!  We'll come back to *object semantics* later.


.. _tut-firststeps:

First Steps Towards Programming
===============================

Of course, we can use Python for more complicated tasks than adding two and two
together.  For instance, we can write an initial sub-sequence of the *Fibonacci*
series as follows::

   >>> # Fibonacci series:
   ... # the sum of two elements defines the next
   ... a, b = 0, 1
   >>> while b < 10:
   ...     print b
   ...     a, b = b, a+b
   ...
   1
   1
   2
   3
   5
   8

This example introduces several new features.

* The first line contains a *multiple assignment*: the variables ``a`` and ``b``
  simultaneously get the new values 0 and 1.  On the last line this is used again,
  demonstrating that the expressions on the right-hand side are all evaluated
  first before any of the assignments take place.  The right-hand side expressions
  are evaluated  from the left to the right.

* The :keyword:`while` loop executes as long as the condition (here: ``b < 10``)
  remains true.  In Python, like in C, any non-zero integer value is true; zero is
  false.  The condition may also be a string or list value, in fact any sequence;
  anything with a non-zero length is true, empty sequences are false.  The test
  used in the example is a simple comparison.  The standard comparison operators
  are written the same as in C: ``<`` (less than), ``>`` (greater than), ``==``
  (equal to), ``<=`` (less than or equal to), ``>=`` (greater than or equal to)
  and ``!=`` (not equal to).

* The *body* of the loop is *indented*: indentation is Python's way of grouping
  statements.  Python does not (yet!) provide an intelligent input line editing
  facility, so you have to type a tab or space(s) for each indented line.  In
  practice you will prepare more complicated input for Python with a text editor;
  most text editors have an auto-indent facility.  When a compound statement is
  entered interactively, it must be followed by a blank line to indicate
  completion (since the parser cannot guess when you have typed the last line).
  Note that each line within a basic block must be indented by the same amount.

* The :keyword:`print` statement writes the value of the expression(s) it is
  given.  It differs from just writing the expression you want to write (as we did
  earlier in the calculator examples) in the way it handles multiple expressions
  and strings.  Strings are printed without quotes, and a space is inserted
  between items, so you can format things nicely, like this::

     >>> i = 256*256
     >>> print 'The value of i is', i
     The value of i is 65536

  A trailing comma avoids the newline after the output::

     >>> a, b = 0, 1
     >>> while b < 1000:
     ...     print b,
     ...     a, b = b, a+b
     ...
     1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987

  Note that the interpreter inserts a newline before it prints the next prompt if
  the last line was not completed.
