.. _tut-morecontrol:

**************************************
Más herramientas para control de flujo
**************************************

Además de la sentencia :keyword:`while` que acabamos de introducir,
Python soporta las sentencias de control de flujo que podemos encontrar en
otros lenguajes, con algunos cambios.


.. _tut-if:

La sentencia :keyword:`if`
==========================

Tal vez el tipo más conocido de sentencia sea el :keyword:`if`. Por
ejemplo::

   >>> x = int(raw_input("Ingresa un entero, por favor: "))
   >>> if x < 0:
   ...      x = 0
   ...      print 'Negativo cambiado a cero'
   ... elif x == 0:
   ...      print 'Cero'
   ... elif x == 1:
   ...      print 'Simple'
   ... else:
   ...      print 'Mas'
   ...

Puede haber cero o más bloques :keyword:`elif`, y el bloque :keyword:`else` es
opcional. La palabra reservada ':keyword:`elif`' es una abreviación de 'else
if', y es útil para evitar un sangrado excesivo. Una secuencia :keyword:`if`
...  :keyword:`elif` ... :keyword:`elif` ... sustituye las sentencias
``switch`` o ``case`` encontradas en otros lenguajes.


.. _tut-for:

La sentencia :keyword:`for`
===========================

.. index::
   statement: for

La sentencia :keyword:`for` en Python difiere un poco de lo que uno puede estar
acostumbrado en lenguajes como C o Pascal.  En lugar de siempre iterar sobre
una progresión aritmética de números (como en Pascal) o darle al usuario la
posibilidad de definir tanto el paso de la iteración como la condición de fin
(como en C), la sentencia :keyword:`for` de Python itera sobre los ítems de
cualquier secuencia (una lista o una cadena de texto), en el orden que aparecen
en la secuencia. Por ejemplo:

.. Aquí se sugirió dar un ejemplo real de C, pero eso solo confundiría a los
   programadores que no saben C.

::

   >>> # Midiendo cadenas de texto
   ... a = ['gato', 'ventana', 'defenestrado']
   >>> for x in a:
   ...     print x, len(x)
   ...
   gato 4
   ventana 7
   defenestrado 12

No es seguro modificar la secuencia sobre la que se está iterando en el lazo
(esto solo es posible para tipos de secuencias mutables, como las listas).  Si
se necesita modificar la lista sobre la que se está iterando (por ejemplo, para
duplicar ítems seleccionados) se debe iterar sobre una copia.  La notación de
rebanada es conveniente para esto::

   >>> for x in a[:]: # hacer una copia por rebanada de toda la lista
   ...    if len(x) > 6: a.insert(0, x)
   ...
   >>> a
   ['defenestrado', 'gato', 'ventana', 'defenestrado']


.. _tut-range:

La función :func:`range`
========================

Si se necesita iterar sobre una secuencia de números, es apropiado utilizar
la función integrada :func:`range`.  Genera una lista conteniendo
progresiones aritméticas::

   >>> range(10)
   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

El valor final dado nunca es parte de la lista; ``range(10)`` genera una lista
de 10 valores, los índices correspondientes para los ítems de una secuencia de
longitud 10. Es posible hacer que el rango empiece con otro número, o
especificar un incremento diferente (incluso negativo; algunas veces se lo
llama 'paso')::

   >>> range(5, 10)
   [5, 6, 7, 8, 9]
   >>> range(0, 10, 3)
   [0, 3, 6, 9]
   >>> range(-10, -100, -30)
   [-10, -40, -70]

Para iterar sobre los índices de una secuencia, se combina :func:`range` y
:func:`len` así::

   >>> a = ['Mary', 'tenia', 'un', 'corderito']
   >>> for i in range(len(a)):
   ...     print i, a[i]
   ...
   0 Mary
   1 tenia
   2 un
   3 corderito


.. _tut-break:

Las sentencias :keyword:`break`, :keyword:`continue`, y :keyword:`else` en lazos
================================================================================

La sentencia :keyword:`break`, como en C, termina el lazo :keyword:`for` o
:keyword:`while` más anidado.

La sentencia :keyword:`continue`, también tomada prestada de C, continua
con la próxima iteración del lazo.

Las sentencias de lazo pueden tener una cláusula ``else`` que es ejecutada
cuando el lazo termina, luego de agotar la lista (con :keyword:`for`) o cuando
la condición se hace falsa (con :keyword:`while`), pero no cuando el lazo es
terminado con la sentencia :keyword:`break`.  Se ejemplifica en el siguiente
lazo, que busca números primos::

   >>> for n in range(2, 10):
   ...     for x in range(2, n):
   ...         if n % x == 0:
   ...             print n, 'es igual a ', x, '*', n/x
   ...             break
   ...     else:
   ...         # sigue el bucle sin encontrar un factor
   ...         print n, 'es un numero primo'
   ...
   2 es un numero primo
   3 es un numero primo
   4 es igual a 2 * 2
   5 es un numero primo
   6 es igual a 2 * 3
   7 es un numero primo
   8 es igual a 2 * 4
   9 es igual a 3 * 3


.. _tut-pass:

La sentencia :keyword:`pass`
============================

La sentencia :keyword:`pass` no hace nada.  Se puede usar cuando una sentencia
es requerida por la sintáxis pero el programa no requiere ninguna acción.
Por ejemplo::

   >>> while True:
   ...       pass # Espera ocupada hasta una interrupción de teclado
   ...


.. _tut-functions:

Definiendo funciones
====================

Podemos crear una función que escriba la serie de Fibonacci hasta un límite
determinado::

   >>> def fib(n):    # escribe la serie de Fibonacci hasta n
   ...     """Escribe la serie de Fibonacci hasta n."""
   ...     a, b = 0, 1
   ...     while b < n:
   ...         print b,
   ...         a, b = b, a+b
   ...
   >>> # Ahora llamamos a la funcion que acabamos de definir:
   ... fib(2000)
   1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597

.. index::
   single: documentation strings
   single: docstrings
   single: strings, documentation

La palabra reservada :keyword:`def` se usa para *definir* funciones.  Debe
seguirle el nombre de la función y la lista de parámetros formales entre
paréntesis.  Las sentencias que forman el cuerpo de la función empiezan en la
línea siguiente, y deben estar con sangría.  La primer sentencia del cuerpo de
la función puede ser opcionalmente una cadena de texto literal; esta es la
cadena de texto de documentación de la función, o :dfn:`docstring`.

Hay herramientas que usan las docstrings para producir automáticamente
documentación en línea o imprimible, o para permitirle al usuario que navegue
el código en forma interactiva; es una buena práctica incluir docstrings en el
código que uno escribe, por lo que se debe intentar hacer un hábito de esto.

La *ejecución* de una función introduce una nueva tabla de símbolos usada para
las variables locales de la función.  Más precisamente, todas las asignaciones
de variables en la función almacenan el valor en la tabla de símbolos local;
así mismo la referencia a variables primero mira la tabla de símbolos local,
luego en la tabla de símbolos local de las funciones externas, luego la tabla
de símbolos global, y finalmente la tabla de nombres predefinidos.  Así, no se
les puede asignar directamente un valor a las variables globales dentro de una
función (a menos se las nombre en la sentencia :keyword:`global`), aunque si
pueden ser referenciadas.

Los parámetros reales (argumentos) de una función se introducen
en la tabla de símbolos local de la función llamada cuando esta es ejecutada;
así, los argumentos son pasados *por valor* (dónde el *valor* es siempre una
*referencia* a un objeto, no el valor del objeto). [#]_ Cuando una función
llama a otra función, una nueva tabla de símbolos local es creada para esa
llamada.

La definición de una función introduce el nombre de la función en la tabla de
símbolos actual.  El valor del nombre de la función tiene un tipo que es
reconocido por el interprete como una función definida por el usuario.  Este
valor puede ser asignado a otro nombre que luego puede ser usado como una
función.  Esto sirve como un mecanismo general para renombrar::

   >>> fib
   <function fib at 10042ed0>
   >>> f = fib
   >>> f(100)
   1 1 2 3 5 8 13 21 34 55 89

Se puede objetar que ``fib`` no es una función, sino un procedimiento.  En
Python, como en C, los procedimientos son solo funciones que no retornan un
valor.  De hecho, técnicamente hablando, los procedimientos sí retornan un
valor, aunque uno aburrido.  Este valor se llama ``None`` (es un nombre
predefinido).  El intérprete por lo general no escribe el valor ``None`` si va
a ser el único valor escrito.  Si realmente se quiere, se puede verlo usando
:keyword:`print`::

   >>> fib(0)
   >>> print fib(0)
   None

Es simple escribir una función que retorne una lista con los números de la
serie de Fibonacci en lugar de imprimirlos::

   >>> def fib2(n): # devuelve la serie de Fibonacci hasta n
   ...     """Devuelve una lista conteniendo la serie de Fibonacci hasta n."""
   ...     result = []
   ...     a, b = 0, 1
   ...     while b < n:
   ...         result.append(b)    # ver abajo
   ...         a, b = b, a+b
   ...     return result
   ...
   >>> f100 = fib2(100)    # llamarla
   >>> f100                # escribir el resultado
   [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

Este ejemplo, como es usual, demuestra algunas características más de Python:

* La sentencia :keyword:`return` devuelve un valor en una función.
  :keyword:`return` sin una expresión como argumento retorna ``None``.  Si se
  alcanza el final de un procedimiento, también se retorna ``None``.

* La sentencia ``result.append(b)`` llama a un *método* del objeto lista
  ``result``.  Un método es una función que 'pertenece' a un objeto y se nombra
  ``obj.methodname``, dónde ``obj`` es algún objeto (puede ser una expresión),
  y ``methodname`` es el nombre del método que está definido por el tipo del
  objeto.  Distintos tipos definen distintos métodos.  Métodos de diferentes
  tipos pueden tener el mismo nombre sin causar ambigüedad.  (Es posible
  definir tipos de objetos propios, y métodos, usando *clases*, como se
  discutirá más adelante en el tutorial).
  El método :meth:`append` mostrado en el ejemplo está definido para objetos
  lista; añade un nuevo elemento al final de la lista.  En este ejemplo es
  equivalente a ``result = result + [b]``, pero más eficiente.


.. _tut-defining:

Más sobre definición de funciones
=================================

También es posible definir funciones con un número variable de argumentos. Hay
tres formas que pueden ser combinadas.


.. _tut-defaultargs:

Argumentos con valores por omisión
----------------------------------

La forma más útil es especificar un valor por omisión para  uno o más
argumentos.  Esto crea una función que puede ser llamada con menos argumentos
que los que permite.  Por ejemplo::

   def pedir_confirmacion(prompt, reintentos=4, queja='Si o no, por favor!'):
       while True:
           ok = raw_input(prompt)
           if ok in ('s', 'S', 'si', 'Si', 'SI'):
               return True
           if ok in ('n', 'no', 'No', 'NO'):
               return False
           reintentos = reintentos - 1
           if reintentos < 0:
               raise IOError('usuario duro')
           print queja

Esta función puede ser llamada tanto así: ``pedir_confirmacion('¿Realmente
queres salir?')`` como así: ``pedir_confirmacion('¿Sobreescribir archivo?',
2)``.

Este ejemplo también introduce la palabra reservada :keyword:`in`, la cual
prueba si una secuencia contiene o no un determinado valor.

Los valores por omisión son evaluados en el momento de la definición de la
función, en el ámbito de la *definición*, entonces::

   i = 5

   def f(arg=i):
       print arg

   i = 6
   f()

...imprimirá ``5``.

**Advertencia importante:**  El valor por omisión es evaluado solo una vez.
Existe una diferencia cuando el valor por omisión es un objeto mutable como una
lista, diccionario, o instancia de la mayoría de las clases.  Por ejemplo, la
siguiente función acumula los argumentos que se le pasan en subsiguientes
llamadas::

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

Si no se quiere que el valor por omisión sea compartido entre subsiguientes
llamadas, se pueden escribir la función así::

   def f(a, L=None):
       if L is None:
           L = []
       L.append(a)
       return L


.. _tut-keywordargs:

Palabras claves como argumentos
-------------------------------

Las funciones también puede ser llamadas nombrando a los argumentos
de la forma ``keyword = value``.  Por ejemplo, la siguiente función::

   def loro(tension, estado='muerto', accion='explotar', tipo='Azul Nordico'):
       print "-- Este loro no va a", accion,
       print "si le aplicas", voltage, "voltios."
       print "-- Gran plumaje tiene el", tipo
       print "-- Esta", estado, "!"

...puede ser llamada de cualquiera de las siguientes formas::

   loro(1000)
   loro(accion='EXPLOTARRRRR', tension=1000000)
   loro('mil', estado='boca arriba')
   loro('un millon', 'rostizado', 'saltar')

...pero estas otras llamadas serían todas inválidas::

   loro()                      # falta argumento obligatorio
   loro(tension=5.0, 'muerto') # argumento nombrado seguido de uno posicional
   loro(110, tension=220)      # valor duplicado para argumento
   loro(actor='Juan Garau')    # palabra clave desconocida

En general, una lista de argumentos debe tener todos sus argumentos
posicionales seguidos por los argumentos nombrados, dónde las palabras
claves deben ser elegidas entre los nombres de los parámetros formales.  No es
importante si un parámetro formal tiene un valor por omisión o no.  Ningún
argumento puede recibir un valor más de una vez (los nombres de parámetros
formales correspondientes a argumentos posicionales no pueden ser usados como
palabras clave en la misma llamada).  Aquí hay un ejemplo que falla debido a
esta restricción::

   >>> def funcion(a):
   ...     pass
   ...
   >>> funcion(0, a=0)
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: function() got multiple values for keyword argument 'a'

Cuando un parámetro formal de la forma ``**nombre`` está presente al final,
recibe un diccionario (ver :ref:`typesmapping`) conteniendo todos los
argumentos nombrados excepto aquellos correspondientes a un parámetro formal.
Esto puede ser combinado con un parámetro formal de la forma ``*nombre``
(descripto en la siguiente sección) que recibe una tupla conteniendo los
argumentos posicionales además de la lista de parámetros formales. (``*nombre``
debe ocurrir antes de ``**nombre``).  Por ejemplo, si definimos una función
así::

   def ventadequeso(tipo, *argumentos, **palabrasclaves):
       print "-- ¿Tiene", tipo, '?'
       print "-- Lo siento, nos quedamos sin", kind
       for arg in argumentos:
           print arg
       print '-'*40
       claves = palabrasclaves.keys()
       claves.sort()
       for c in claves:
           print c, ':', palabrasclaves[c]

Puede ser llamada así::

   ventadequeso('Limburger', "Es muy liquido, sr.",
              "Realmente es muy muy liquido, sr.",
              cliente='Juan Garau',
              vendedor='Miguel Paez',
              puesto='Venta de Queso Argentino')

...y por supuesto imprimirá::

   -- ¿Tiene Limburger ?
   -- Lo siento, nos quedamos sin Limburger
   Es muy liquido, sr.
   Realmente es muy muy liquido, sr.
   ----------------------------------------
   cliente : Juan Garau
   vendedor : Miguel Paez
   puesto : Venta de Queso Argentino

Se debe notar que el método :meth:`sort` de la lista de nombres de argumentos
nombrados es llamado antes de imprimir el contenido del diccionario
``palabrasclaves``; si esto no se hace, el orden en que los argumentos son
impresos no está definido.

.. _tut-arbitraryargs:

Listas de argumentos arbitrarios
--------------------------------

.. index::
  statement: *

Finalmente, la opción menos frecuentemente usada es especificar que una
función puede ser llamada con un número arbitrario de argumentos.  Estos
argumentos serán organizados en una tupla.  Antes del número variable de
argumentos, cero o más argumentos normales pueden estar presentes.::

   def fprintf(file, template, *args):
       file.write(template.format(args))


.. _tut-unpacking-arguments:

Desempaquetando una lista de argumentos
---------------------------------------

La situación inversa ocurre cuando los argumentos ya están en una lista o
tupla pero necesitan ser desempaquetados para llamar a una función que
requiere argumentos posicionales separados.  Por ejemplo, la función
predefinida :func:`range` espera los argumentos *inicio* y *fin*.  Si no están
disponibles en forma separada, se puede escribir la llamada a la función con
el operador para desempaquetar argumentos de una lista o una tupla ``*``\::

   >>> range(3, 6)       # llamada normal con argumentos separados
   [3, 4, 5]
   >>> args = [3, 6]
   >>> range(*args)      # llamada con argumentos desempaquetados de una lista
   [3, 4, 5]

.. index::
  statement: **

Del mismo modo, los diccionarios pueden entregar argumentos nombrados
con el operador ``**``\::

   >>> def loro(tension, estado='rostizado', accion='explotar'):
   ...     print "-- Este loro no va a", accion,
   ...     print "si le aplicas", voltage, "voltios.",
   ...     print "Esta", estado, "!"
   ...
   >>> d = {"tension": "cuatro millones", "estado": "demacrado",
            "accion": "VOLAR"}
   >>> loro(**d)
   -- Este loro no va a VOLAR si le aplicas cuatro millones
      voltios. Esta demacrado !


.. _tut-lambda:

Formas con lambda
-----------------

Por demanda popular, algunas características comúnmente encontradas en
lenguajes de programación funcionales como Lisp fueron añadidas a Python.  Con
la palabra reservada :keyword:`lambda` se pueden crear pequeñas funciones
anónimas.  Esta es una función que devuelve la suma de sus dos argumentos:
``lambda a, b: a+b``.  Las formas con lambda pueden ser usadas en cualquier
lugar que se requieran funciones.  Semánticamente, son solo azúcar sintáctica
para la definición de funciones.  Cómo en la definición de funciones anidadas,
las formas con lambda pueden hacer referencia a variables del ámbito en el que
son contenidas::

   >>> def hacer_incrementador(n):
   ...     return lambda x: x + n
   ...
   >>> f = hacer_incrementador(42)
   >>> f(0)
   42
   >>> f(1)
   43


.. _tut-docstrings:

Cadenas de texto de documentación
---------------------------------

.. index::
   single: docstrings
   single: documentation strings
   single: strings, documentation

Hay convenciones emergentes sobre el contenido y formato de las cadenas de
texto de documentación.

La primer línea debe ser siempre un resumen corto y conciso del propósito del
objeto. Para ser breve, no se debe mencionar explícitamente el nombre o tipo
del objeto, ya que estos están disponibles de otros modos (excepto si el nombre
es un verbo que describe el funcionamiento de la función). Esta línea debe
empezar con una letra mayúscula y terminar con un punto.

Si hay más líneas en la cadena de texto de documentación, la segunda línea debe
estar en blanco, separando visualmente el resumen del resto de la descripción.
Las líneas siguientes deben ser uno o más párrafos describiendo las
convenciones para llamar al objeto, efectos secundarios, etc.

El analizador de Python no quita la identación de las cadenas de texto
literales multi-líneas, entonces las herramientas que procesan documentación
tienen que quitar la identación si así lo quieren. Esto se hace mediante la
siguiente convención. La primer línea que no está en blanco *siguiente* a la
primer línea de la cadena determina la cantidad de identación para toda la
cadena de documentación. (No podemos usar la primer línea ya que generalmente
es adyacente a las comillas de apertura de la cadena y la identación no se nota
en la cadena de texto). Los espacios en blanco "equivalentes" a esta identación
son luego quitados del comienzo de cada línea en la cadena. No deberían haber
líneas con menor identación, pero si las hay todos los espacios en blanco del
comienzo deben ser quitados. La equivalencia de espacios en blanco debe ser
verificada luego de la expansión de tabs (a 8 espacios, normalmente).

Este es un ejemplo de un docstring multi-línea::

   >>> def mi_funcion():
   ...     """No hace mas que documentar la funcion.
   ...
   ...     No, de verdad. No hace nada.
   ...     """
   ...     pass
   ...
   >>> print mi_funcion.__doc__
   No hace mas que documentar la funcion.

   No, de verdad. No hace nada.


.. _tut-codingstyle:

Intermezzo: Estilo de Codificación
==================================

.. sectionauthor:: Georg Brandl <georg@python.org>
.. index:: pair: coding; style

Ahora que estás a punto de escribir piezas de Python más largas y complejas,
es un buen momento para hablar sobre *estilo de codificación*. La mayoría de
los lenguajes pueden ser escritos (o mejor dicho, *formateados*) con diferentes
estilos; algunos son mas fáciles de leer que otros. Hacer que tu código sea más
fácil de leer por otros es siempre una buena idea, y adoptar un buen estilo de
codificación ayuda tremendamente a lograrlo.

Para Python, :pep:`8` se erigió como la guía de estilo a la que más proyectos
adhirieron; promueve un estilo de codificación fácil de leer y amable con los
ojos. Todos los desarrolladores Python deben leerlo en algún momento; aquí
están extraídos los puntos más importantes:

* Usar identación de 4 espacios, no tabs.

  4 espacios son un buen compromiso entre identación pequeña (permite mayor
  nivel de identación) e identación grande (más fácil de leer). Los tabs
  introducen confusión y es mejor dejarlos de lado.

* Recortar las líneas para que no superen los 79 caracteres.

  Esto ayuda a los usuarios con pantallas pequeñas y hace posible tener varios
  archivos de código abiertos, uno al lado del otro, en pantallas grandes.

* Usar líneas en blanco para separar funciones y clases, y bloques grandes
  de código dentro de funciones.

* Cuando sea posible, poner comentarios en una sola línea.

* Usar docstrings.

* Usar espacios alrededor de operadores y luego de las comas, pero no
  directamente dentro de paréntesis: ``a = f(1, 2) + g(3, 4)``.

* Nombrar las clases y funciones consistentemente; la convención es usar
  ``NotacionCamello`` para clases y ``minusculas_con_guiones_bajos`` para
  funciones y métodos. Siempre usar ``self`` como el nombre para el primer
  argumento en los métodos.

* No usar codificaciones estrafalarias si se espera usar el código en entornos
  internacionales. ASCII plano funciona bien en la mayoría de los casos.


.. rubric:: Footnotes

.. [#] En realidad, *llamadas por referencia de objeto* sería una
   mejordescripción, ya que si un objeto mutable es pasado, quien realiza la
   llamaba verá cualquier cambio que el llamado realice sobre el mismo (como
   ítems insertados en una lista).


