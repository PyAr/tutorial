.. _tut-structures:

********************
Estructuras de datos
********************

Este capítulo describe algunas cosas que ya aprendiste en más detalle,
y agrega algunas cosas nuevas también.


.. _tut-morelists:

Más sobre listas
================

El tipo de dato lista tiene algunos métodos más.  Aquí están todos los métodos
de los objetos lista:


.. method:: list.append(x)
   :noindex:

   Agrega un ítem al final de la lista; equivale a ``a[len(a):] = [x]``.


.. method:: list.extend(L)
   :noindex:

   Extiende la lista agregándole todos los ítems de la lista dada; equivale
   a  ``a[len(a):] = L``.


.. method:: list.insert(i, x)
   :noindex:

   Inserta un ítem en una posición dada.  El primer argumento es el índice
   del ítem delante del cual se insertará, por lo tanto ``a.insert(0, x)``
   inserta al principio de la lista, y ``a.insert(len(a), x)`` equivale a
   ``a.append(x)``.


.. method:: list.remove(x)
   :noindex:

   Quita el primer ítem de la lista cuyo calor sea *x*. Es un error si no
   existe tal ítem.


.. method:: list.pop([i])
   :noindex:

   Quita el ítem en la posición dada de la lista, y lo devuelve.  Si no se
   especifica un índice, ``a.pop()`` quita y devuelve el último ítem de la
   lista.  (Los corchetes que encierran a *i* en la firma del método) denotan
   que el parámetro es opcional, no que deberías escribir corchetes en esa
   posición.  Verás esta notación con frecuencia en la Referencia de la
   Biblioteca de Python.)


.. method:: list.index(x)
   :noindex:

   Devuelve el índice en la lista del primer ítem cuyo valor sea *x*. Es un
   error si no existe tal ítem.

.. method:: list.count(x)
   :noindex:

   Devuelve el número de veces que *x* aparece en la lista.


.. method:: list.sort()
   :noindex:

   Ordena los ítems de la lista, in situ.


.. method:: list.reverse()
   :noindex:

   Invierte los elementos de la lista, in situ.

Un ejemplo que usa la mayoría de los métodos de lista::

   >>> a = [66.25, 333, 333, 1, 1234.5]
   >>> print a.count(333), a.count(66.25), a.count('x')
   2 1 0
   >>> a.insert(2, -1)
   >>> a.append(333)
   >>> a
   [66.25, 333, -1, 333, 1, 1234.5, 333]
   >>> a.index(333)
   1
   >>> a.remove(333)
   >>> a
   [66.25, -1, 333, 1, 1234.5, 333]
   >>> a.reverse()
   >>> a
   [333, 1234.5, 1, 333, -1, 66.25]
   >>> a.sort()
   >>> a
   [-1, 1, 66.25, 333, 333, 1234.5]


.. _tut-lists-as-stacks:

Usando listas como pilas
------------------------

.. sectionauthor:: Ka-Ping Yee <ping@lfw.org>


Los métodos de lista hacen que resulte muy fácil usar una lista como una pila,
donde el último elemento añadido es el primer elemento retirado ("último en
entrar, primero en salir").  Para agregar un ítem a la cima de la pila, use
:meth:`append`. Para retirar un ítem de la cima de la pila, use :meth:`pop`
sin un índice explícito.  Por ejemplo::

   >>> stack = [3, 4, 5]
   >>> stack.append(6)
   >>> stack.append(7)
   >>> stack
   [3, 4, 5, 6, 7]
   >>> stack.pop()
   7
   >>> stack
   [3, 4, 5, 6]
   >>> stack.pop()
   6
   >>> stack.pop()
   5
   >>> stack
   [3, 4]


.. _tut-lists-as-queues:

Usando listas como colas
------------------------

.. sectionauthor:: Ka-Ping Yee <ping@lfw.org>


También puedes usar una lista convenientemente como una cola, donde el primer
elemento añadido es el primer elemento retirado ("primero en entrar, primero
en salir").  Para agregar un ítem al final de la cola, use :meth:`append`.
Para retirar un ítem del frente de la pila, use :meth:`pop` con ``0`` como
índice. Por ejemplo::

   >>> queue = ["Eric", "John", "Michael"]
   >>> queue.append("Terry")           # llega Terry
   >>> queue.append("Graham")          # llega Graham
   >>> queue.pop(0)
   'Eric'
   >>> queue.pop(0)
   'John'
   >>> queue
   ['Michael', 'Terry', 'Graham']


.. _tut-functional:

Herramientas de programación funcional
--------------------------------------

Hay tres funciones integradas que son muy útiles cuando se usan con listas:
:func:`filter`, :func:`map`, y :func:`reduce`.

``filter(funcion, secuencia)`` devuelve una secuencia con aquellos ítems de la
secuencia para los cuales ``funcion(item)`` es verdadero. Si *secuencia* es una
:class:`cadena` o :class:`tupla`, el resultado será del mismo tipo;
de otra manera, siempre es una :class:`lista`. Por ejemplo, para calcular unos
primos::

   >>> def f(x): return x % 2 != 0 and x % 3 != 0
   ...
   >>> filter(f, range(2, 25))
   [5, 7, 11, 13, 17, 19, 23]

``map(funcion, secuencia)`` llama a ``funcion(item)`` por cada uno de los
ítems de la secuencia y devuelve una lista de los valores retornados.  Por
ejemplo, para calcular unos cubos::

   >>> def cubo(x): return x*x*x
   ...
   >>> map(cubo, range(1, 11))
   [1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]

Se puede pasar más de una secuencia; la función debe entonces tener tantos
argumentos como secuencias haya y es llamada con el ítem correspondiente de
cada secuencia (o ``None`` si alguna secuencia es más corta que otra).  Por
ejemplo::

   >>> sec = range(8)
   >>> def add(x, y): return x+y
   ...
   >>> map(add, sec, sec)
   [0, 2, 4, 6, 8, 10, 12, 14]

``reduce(funcion, secuencia)`` devuelve un único valor que se construye
llamando a la función binaria *funcion* con los primeros dos ítems de la
secuencia, entonces con el resultado y el siguiente ítem, y así sucesivamente.
Por ejemplo, para calcular la suma de los números de 1 a 10::

   >>> def sumar(x,y): return x+y
   ...
   >>> reduce(sumar, range(1, 11))
   55

Si sólo hay un ítem en la secuencia, se devuelve su valor; si la secuencia
está vacía, se lanza una excepción.

Un tercer argumento puede pasarse para indicar el valor inicial.  En este caso
el valor inicial se devuelve para una secuencia vacía, y la función se aplica
primero al valor inicial y el primer ítem de la secuencia, entonces al
resultado y al siguiente ítem, y así sucesivamente. Por ejemplo, ::

   >>> def sum(sec):
   ...     def sumar(x,y): return x+y
   ...     return reduce(sumar, sec, 0)
   ...
   >>> sum(range(1, 11))
   55
   >>> sum([])
   0

No uses la definicón de este ejemplo de :func:`sum`: ya que la sumatoria es una
necesidad tan común, una función integrada ``sum(secuencia)`` ya es provista,
y funciona exactamente así.

.. versionadded:: 2.3


Listas por comprensión
----------------------

Las listas por comprensión proveen una forma concisa de crear listas sin tener
que recurrir al uso de :func:`map`, :func:`filter` y/o :keyword:`lambda`. La
definición resultante de la lista a menudo tiende a ser más clara que las
listas formadas usando esas construcciones.
Cada lista por comprensión consiste de una expresión seguida por una cláusula
:keyword:`for`, luego cero o más cláusulas :keyword:`for` o :keyword:`if`. El
resultado será una lista que resulta de evaluar la expresión en el contexto de
las cláusulas :keyword:`for` y :keyword:`if` que sigan.  Si la expresión
evaluase a una tupla, debe encerrarse entre paréntesis. ::

   >>> frutafresca = ['  banana', '  mora de Logan ', 'maracuya  ']
   >>> [arma.strip() for arma in frutafresca]
   ['banana', 'mora de logan', 'maracuya']
   >>> vec = [2, 4, 6]
   >>> [3*x for x in vec]
   [6, 12, 18]
   >>> [3*x for x in vec if x > 3]
   [12, 18]
   >>> [3*x for x in vec if x < 2]
   []
   >>> [[x,x**2] for x in vec]
   [[2, 4], [4, 16], [6, 36]]
   >>> [x, x**2 for x in vec]	# error - se requieren paréntesis para tuplas
     File "<stdin>", line 1, in ?
       [x, x**2 for x in vec]
                  ^
   SyntaxError: invalid syntax
   >>> [(x, x**2) for x in vec]
   [(2, 4), (4, 16), (6, 36)]
   >>> vec1 = [2, 4, 6]
   >>> vec2 = [4, 3, -9]
   >>> [x*y for x in vec1 for y in vec2]
   [8, 6, -18, 16, 12, -36, 24, 18, -54]
   >>> [x+y for x in vec1 for y in vec2]
   [6, 5, -7, 8, 7, -5, 10, 9, -3]
   >>> [vec1[i]*vec2[i] for i in range(len(vec1))]
   [8, 12, -54]

Las listas por comprensión son mucho más flexibles que :func:`map` y pueden
aplicarse a expresiones complejas y funciones anidadas::

   >>> [str(round(355/113.0, i)) for i in range(1,6)]
   ['3.1', '3.14', '3.142', '3.1416', '3.14159']


Listas por comprensión anidadas
-------------------------------

Si tienes el estómago suficiente, las listas por comprensión pueden anidarse.
Son una herramienta poderosa pero -- como toda herramienta poderosa -- deben
usarse con cuidado, o ni siquiera usarse.

Considera el siguiente ejemplo de una matriz de 3x3 como una lista que
contiene tres listas, una por fila::

    >>> mat = [
    ...        [1, 2, 3],
    ...        [4, 5, 6],
    ...        [7, 8, 9],
    ...       ]

Ahora, si quisieras intercambiar filas y columnas, podrías usar una lista por
comprensión::

    >>> print [[fila[i] for fila in mat] for i in [0, 1, 2]]
    [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

Se debe tener cuidado especial para la lista por comprensión *anidada*:

    Para evitar aprensión cuando se anidan lista por comprensión, lee de
    derecha a izquierda.

Una versión más detallada de este retazo muestra el flujo de manera
explícita::

    for i in [0, 1, 2]:
        for fila in mat:
            print fila[i],
        print

En el mundo real, deberías preferir funciones predefinidas a declaraciones con
flujo complejo. La función :func:`zip` haría un buen trabajo para este caso de
uso::

    >>> zip(*mat)
    [(1, 4, 7), (2, 5, 8), (3, 6, 9)]

Ver :ref:`tut-unpacking-arguments` para detalles en el asterisco de esta línea.

.. _tut-del:

La instrucción :keyword:`del`
============================

Hay una manera de quitar un ítem de una lista dado su índice en lugar de su
valor: la instrucción :keyword:`del`. Ésta es diferente del método :meth:`pop`,
el cual devuelve un valor.  La instrucción :keyword:`del` también puede usarse
para quitar secciones de una lista o vaciar la lista completa (lo que hacíamos
antes asignando una lista vacía a la sección).  Por ejemplo::

   >>> a = [-1, 1, 66.25, 333, 333, 1234.5]
   >>> del a[0]
   >>> a
   [1, 66.25, 333, 333, 1234.5]
   >>> del a[2:4]
   >>> a
   [1, 66.25, 1234.5]
   >>> del a[:]
   >>> a
   []

:keyword:`del` puede usarse también para eliminar variables::

   >>> del a

Referenciar al nombre ``a`` de aquí en más es un error (al menos hasta que se
le asigne otro valor).  Veremos otros usos para :keyword:`del` más adelante.


.. _tut-tuples:

Tuplas y secuencias
===================

Vimos que las listas y cadenas tienen propiedades en común, como el indexado y
las operaciones de seccionado.  Éstas son dos ejemplos de datos de tipo
*secuencia* (ver :ref:`typesseq`).  Como Python es un lenguaje en evolución,
otros datos de tipo secuencia pueden agregarse.  Existe otro dato de tipo
secuencia estándar: la *tupla*.

Una tupla consiste de un número de valores separados por comas, por ejemplo::

   >>> t = 12345, 54321, 'hola!'
   >>> t[0]
   12345
   >>> t
   (12345, 54321, 'hola!')
   >>> # Las tuplas pueden anidarse:
   ... u = t, (1, 2, 3, 4, 5)
   >>> u
   ((12345, 54321, 'hola!'), (1, 2, 3, 4, 5))

Como puedes ver, en la salida las tuplas siempre se encierran entre paréntesis,
para que las tuplas anidadas puedan interpretarse correctamente; pueden
ingresarse con o sin paréntesis, aunque a menudo los paréntesis son necesarios
de todas formas (si la tupla es parte de una expresión más grande).

Las tuplas tienen muchos usos.  Por ejemplo: pares ordenados (x, y), registros
de empleados de una base de datos, etc.  Las tuplas, al igual que las cadenas,
son inmutables: no es posible asignar a los ítems individuales de una tupla
(aunque puedes simular bastante ese efecto mediante seccionado y
concatenación).  También es posible crear tuplas que contengan objetos mutables
como listas.

Un problema particular es la construcción de tuplas que contengan 0 o 1 ítem:
la sintaxis presenta algunas peculiaridades para estos casos.  Las tuplas
vacías se construyen mediante un par de paréntesis vacío; una tupla con un ítem
se construye poniendo una coma a continuación del valor (no alcanza con
encerrar un único valor entre paréntesis). Feo, pero efectivo.  Por ejemplo::

   >>> vacia = ()
   >>> singleton = 'hola',    # <-- notar la coma al final
   >>> len(vacia)
   0
   >>> len(singleton)
   1
   >>> singleton
   ('hola',)

La declaración ``t = 12345, 54321, 'hola!'`` es un ejemplo de *empaquetado de
tuplas*: los valores ``12345``, ``54321`` y ``'hola!'`` se empaquetan juntos en
una tupla.
La operación inversa también es posible::

   >>> x, y, z = t

Esto se llama, apropiadamente, *desempaquetado de secuencias*. El
desempaquetado de secuencias requeire que la lista de variables a la izquierda
tenga el mismo número de elementos que el tamaño de la secuencia.  ¡Nota que
la asignación múltiple es en realidad sólo una combinación de empaquetado de
tuplas y desempaquetado de secuencias!

Hay una pequeña asimetría aquí:  empaquetando múltiples valores siempre crea
una tupla, y el desempaquetado funciona con cualquier secuencia.

.. XXX Agrega un poco sobre la diferencia entre tuplas y listas.


.. _tut-sets:

Conjuntos
=========

Python también incluye un tipo de dato para *conjuntos*.  Un conjunto es una
colección no ordenada y sin elementos repetidos.  Los usos básicos de éstos
incluyen verificación de pertenencia y eliminación de entradas duplicadas.
Los conjuntos también soportan operaciones matemáticas como la unión,
intersección, diferencia, y diferencia simétrica.

Una pequeña demostración::

   >>> canasta = ['manzana', 'naranja', 'manzana', 'pera', 'naranja', 'banana']
   >>> fruta = set(canasta)               # crea un conjunto sin repetidos
   >>> fruta
   set(['naranja', 'pera', 'manzana', 'banana'])
   >>> 'naranja' in fruta                 # verificación de pertenencia rápida
   True
   >>> 'yerba' in fruta
   False

   >>> # Veamos las operaciones de conjuntos para las letras únicas de dos palabras
   ...
   >>> a = set('abracadabra')
   >>> b = set('alacazam')
   >>> a                                  # letras únicas en a
   set(['a', 'r', 'b', 'c', 'd'])
   >>> a - b                              # letras en a pero no en b
   set(['r', 'd', 'b'])
   >>> a | b                              # letras en a o en b
   set(['a', 'c', 'r', 'd', 'b', 'm', 'z', 'l'])
   >>> a & b                              # letras en a y en b
   set(['a', 'c'])
   >>> a ^ b                              # letras en a o b pero no en ambos
   set(['r', 'd', 'b', 'm', 'z', 'l'])


.. _tut-dictionaries:

Diccionarios
============

Otro tipo de dato útil incluído en Python es el *diccionario* (ver
:ref:`typesmapping`). Los diccionarios se encuentran a veces en otros lenguajes
como "memorias asociativas" o "arreglos asociativos". A diferencia de las
secuencias, que se indexan mediante un rango numérico, los diccionarios se
indexan con *claves*, que pueden ser cualquier tipo inmutable; las cadenas y
números siempre pueden ser claves.  Las tuplas pueden usarse como claves si
solamente contienen cadenas, números o tuplas; si una tupla contiene cualquier
objeto mutable directa o indirectamente, no puede usarse como clave.
No puedes usar listas como claves, ya que las listas pueden modificarse usando
asignación por índice, asignación por sección, o métodos como :meth:`append` y
:meth:`extend`.

Lo mejor es pensar en un diccionario como un conjunto no ordenado de pares
*clave: valor*, con el requerimiento de que las claves sean únicas (dentro de
un diccionario en particular). Un par de llaves crean un diccionario vacío:
``{}``. Colocar una lista de pares clave:valor separados por comas entre las
llaves añade pares clave:valor iniciales al diccionario; esta también es la
forma en que los diccionarios se presentan en la salida.

Las operaciones principales sobre un diccionario son guardar un valor con una
clave y extraer ese valor dada la clave.  También es posible borrar un par
clave:valor con ``del``. Si usas una clave que ya está en uso para guardar un
valor, el valor que estaba asociado con esa clave se pierde.  Es un error
extraer un valor usando una clave no existente.

El método :meth:`keys` de un diccionario devuelve una lista de todas las claves
en uso de ese diccionario, en un orden arbitrario (si la quieres ordenada,
simplemente usa el metodo :meth:`sort` sobre la lista de claves).  Para
verificar si una clave está en el diccionario, utiliza la palabra clave
:keyword:`in`.

Un pequeño ejemplo de uso de un diccionario::

   >>> tel = {'jack': 4098, 'sape': 4139}
   >>> tel['guido'] = 4127
   >>> tel
   {'sape': 4139, 'guido': 4127, 'jack': 4098}
   >>> tel['jack']
   4098
   >>> del tel['sape']
   >>> tel['irv'] = 4127
   >>> tel
   {'guido': 4127, 'irv': 4127, 'jack': 4098}
   >>> tel.keys()
   ['guido', 'irv', 'jack']
   >>> 'guido' in tel
   True

El constructor :func:`dict` crea un diccionario directamente desde listas de
pares clave-valor guardados como tuplas.  Cuando los pares siguen un patrón,
se puede especificar de forma compacta la lista de pares clave-valor por
comprensión. ::

   >>> dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
   {'sape': 4139, 'jack': 4098, 'guido': 4127}
   >>> dict([(x, x**2) for x in (2, 4, 6)])     # use a list comprehension
   {2: 4, 4: 16, 6: 36}

Más adelante en este tutorial, aprenderemos acerca de Expresiones Generadoras
que están mejor preparadas para la tarea de proveer pares clave-valor al constructor
:func:`dict`.

Cuando las claves son cadenas simples, a veces resulta más fácil especificar
los pares usando argumentos por palabra clave::

   >>> dict(sape=4139, guido=4127, jack=4098)
   {'sape': 4139, 'jack': 4098, 'guido': 4127}


.. _tut-loopidioms:

Técnicas de iteración
=====================

Cuando iteramos sobre diccionarios, se pueden obtener al mismo tiempo la clave
y su valor correspondiente usando el método :meth:`iteritems`. ::

   >>> caballeros = {'gallahad': 'el puro', 'robin': 'el valiente'}
   >>> for k, v in knights.iteritems():
   ...     print k, v
   ...
   gallahad el puro
   robin el valiente

Cuando se itera sobre una secuencia, se puede obtener el índice de posición
junto a su valor correspondiente usando la función :func:`enumerate`. ::

   >>> for i, v in enumerate(['ta', 'te', 'ti']):
   ...     print i, v
   ...
   0 ta
   1 te
   2 ti

Para iterar sobre dos o más secuencias al mismo tiempo, los valores pueden
emparejarse con la función :func:`zip`. ::

   >>> preguntas = ['nombre', 'mision', 'color favorito']
   >>> respuestas = ['lancelot', 'el santo grial', 'azul']
   >>> for p, r in zip(preguntas, respuestas):
   ...     print 'Cual es tu {0}?  {1}.'.format(p, r)
   ...	
   Cual es tu nombre?  lancelot.
   Cual es tu mision?  el santo grial.
   Cual es tu color favorito?  azul.

Para iterar sobre una secuencia en orden inverso, se especifica primero la
secuencia al derecho y luego se llama a la función :func:`reversed`. ::

   >>> for i in reversed(xrange(1,10,2)):
   ...     print i
   ...
   9
   7
   5
   3
   1

Para iterar sobre una secuencia ordenada, se utiliza la función :func:`sorted`
la cual devuelve una nueva lista ordenada dejando a la original intacta. ::

   >>> canasta = ['manzana', 'naranja', 'manzana', 'pera', 'naranja', 'banana']
   >>> for f in sorted(set(canasta)):
   ...     print f
   ... 	
   banana
   manzana
   naranja
   pera


.. _tut-conditions:

Más acerca de condiciones
=========================

Las condiciones usadas en las instrucciones ``while`` e ``if`` pueden contener
cualquier operador, no sólo comparaciones.

Los operadores de comparación ``in`` y ``not in`` verifican si un valor está
(o no está) en una secuencia. Los operadores ``is`` e ``is not`` comparan si
dos objetos son realmente el mismo objeto; esto es significativo sólo para
objetos mutables como las listas.  Todos los operadores de comparación tienen
la misma prioridad, la cual es menor que la de todos los operadores numéricos.

Las comparaciones pueden encadenarse.  Por ejemplo, ``a < b == c`` verifica si
``a`` es menor que ``b`` y además si ``b`` es igual a ``c``.

Las comparaciones pueden combinarse mediante los operadores Booleanos ``and`` y
``or``, y el resultado de una comparación (o de cualquier otra expresión
Booleana) puede negarse con ``not``.  Éstos tienen prioridades menores que los
operadores de comparación; entre ellos ``not`` tienen la mayor prioridad y
``or`` la menor, o sea que ``A and not B or C`` equivale a
``(A and (not B)) or C``. Como siempre, los paréntesis pueden usarse para
expresar la composición deseada.

Los operadores Booleanos ``and`` y ``or`` son los llamados operadores
*cortocircuito*: sus argumentos se evalúan de izquierda a derecha, y la
evaluación se detiene en el momento en el que se determina su resultado. Por
ejemplo, si ``A`` y ``C`` son verdaderas pero ``B`` es falsa, en
``A and B and C`` no se evalúa la expresión ``C``.  Cuando se usa como un valor
general y no como un Booleano, el valor devuelto de un operador cortocircuito
es el último argumento evaluado.

Es posible asignar el resultado de una comparación u otra expresión Booleana a
una variable.  Por ejemplo, ::

   >>> cadena1, cadena2, cadena3 = '', 'Trondheim', 'Paso Hammer'
   >>> non_nulo = cadena1 or cadena2 or cadena3
   >>> non_nulo
   'Trondheim'

Nota que en Python, a diferencia de C, la asignación no puede ocurrir dentro de
expresiones. Los programadores de C pueden renegar por esto, pero es algo que
evita un tipo de problema común encontrado en programas en C: escribir ``=`` en
una expresión cuando lo que se quiere escribir es ``==``.


.. _tut-comparing:

Comparando secuencias y otros tipos
===================================

Las secuencias pueden compararse con otros objetos del mismo tipo de secuencia.
La comparación usa orden *lexicográfico*: primero se comparan los dos primeros
ítems, si son diferentes esto ya determina el resultado de la comparación; si
son iguales, se comparan los siguientes dos ítems, y así sucesivamente hasta
llegar al final de alguna de las secuencias. Si dos ítems a comparar son ambos
secuencias del mismo tipo, la comparación lexicográfica es recursiva.  Si todos
los ítems de dos secuencias resultan iguales, se considera que las secuencias
son iguales.
Si una secuencia es una subsecuencia inicial de la otra, la secuencia más corta
es la menor. El orden lexicográfico para cadenas de caracteres utiliza el orden
ASCII para caracteres individuales.  Algunos ejemplos de comparaciones entre
secuencias del mismo tipo::

   (1, 2, 3)              < (1, 2, 4)
   [1, 2, 3]              < [1, 2, 4]
   'ABC' < 'C' < 'Pascal' < 'Python'
   (1, 2, 3, 4)           < (1, 2, 4)
   (1, 2)                 < (1, 2, -1)
   (1, 2, 3)             == (1.0, 2.0, 3.0)
   (1, 2, ('aa', 'ab'))   < (1, 2, ('abc', 'a'), 4)

Observa que comparar objetos de diferentes tipos es legal. El resultado es
determinístico pero arbitrario: los tipos se ordenan por su nombre. Por lo
tanto, una lista siempre evalúa como menor que una cadena (nota del t.:
list < string), etc.
[#]_ Tipos numéricos diferentes se comparan a su valor numérico, o sea 0 es
igual a 0.0, etc.


.. rubric:: Footnotes

.. [#] No confiar demasiado en las reglas para comparar objetos de diferentes
tipos; pueden cambiar en una versión futura del lenguaje.

