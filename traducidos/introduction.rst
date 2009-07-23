.. _tut-informal:

**********************************
Una introducción informal a Python
**********************************

En los siguientes ejemplos, las entradas y salidas son distinguidas por la
presencia o ausencia de los prompts (```>>>``` and ```...```): para
reproducir los ejemplos, debés escribir todo lo que esté después del prompt,
cuando este aparezca; las líneas que no comiencen con el prompt son las
salidas del intérprete.  Tené en cuenta que el prompt secundario que
aparece por si sólo en una línea de un ejemplo significa que debés escribir
una línea en blanco; esto es usado para terminar un comando multilínea.

Muchos de los ejemplos de este manual, incluso aquellos ingresados en el prompt
interactivo, incluyen comentarios.  Los comentarios en Python comienzan con
el carácter numeral, ``#``, y se extienden hasta el final físico de la
línea.  Un comentario quizás aparezca al comienzo de la línea o seguidos
de espacios blancos o código, pero sin una cadena de caracteres.
Un carácter numeral dentro de una cadena de caracteres es sólo un carácter
numeral.

Algunos ejemplos::

   # este es el primer comentario
   SPAM = 1                 # y este es el segundo comentario
                            # ... y ahora un tercero!
   STRING = "# Este no es un comentario".


.. _tut-calculator:

Usar Python como una calculadora
================================

Vamos a probar algunos comandos simples en Python.  Iniciá un intérprete y
esperá por el prompt primario, ``>>>``. (No debería demorar tanto).

.. _tut-numbers:

Números
-------

El intérprete actúa como una simple calculadora; podés ingrsar una expresión
y este escribirá los valores.  La sintaxis es sencilla: los operadores ``+``,
``-``, ``*`` y ``/`` funcionan como en la mayoría de los lenguajes (por
ejemplo, Pascal o C); los paréntesis pueden ser usados para agrupar. Por
ejemplo::

   >>> 2+2
   4
   >>> # Este es un comentario
   ... 2+2
   4
   >>> 2+2  # y un comentario en la misma línea que el código
   4
   >>> (50-5*6)/4
   5
   >>> # La división entera retorna redondeado al piso:
   ... 7/3
   2
   >>> 7/-3
   -3

El signo igual (``=``) es usado para asignar un valor a una variable.  Luego,
ningún resultado es mostrado antes del próximo prompt::

   >>> ancho = 20
   >>> largo = 5*9
   >>> ancho * largo
   900

Un valor puede ser asignado a varias variables simultáneamente::

   >>> x = y = z = 0  # Cero a x, y, y z
   >>> x
   0
   >>> y
   0
   >>> z
   0

Se soporta completamente los números de punto flotante; las operaciones con
mezclas en los tipos de los operandos convierten los enteros a punto flotante::

   >>> 3 * 3.75 / 1.5
   7.5
   >>> 7.0 / 2
   3.5

Los números complejos también están soportados; los números imaginarios son
escritos con el sufijo de ``j`` o ``J``.  Los números complejos con un
componente real que no sea cero son escritos como ``(real+imagj)``, o pueden
ser escrito con la función ``complex(real, imag)``. ::

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
flotante, la parte real y la imaginaria.  Para extraer estas partes desde un
número complejo *z*, usá ``z.real`` y ``z.imag``. ::

   >>> a=1.5+0.5j
   >>> a.real
   1.5
   >>> a.imag
   0.5

La función de conversión de los punto flotante y enteros (:func:`float`,
:func:`int` y :func:`long`) no funciona para números complejos; aquí no hay
una forma correcta de convertir un número complejo a un número real.  Usá
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

En el modo interactivo, la última expresión impresa es asignada a la variable
``_``.  Esto significa que cuando estés usando Python como una calculadora de
escritorio, es más fácil seguir calculando, por ejemplo::

   >>> impuesto = 12.5 / 100
   >>> precio = 100.50
   >>> precio * impuesto
   12.5625
   >>> precio + _
   113.0625
   >>> round(_, 2)
   113.06
   >>>

Esta variable debería ser tratada como de sólo lectura por el usuario.  No le
asignes explícitamente un valor; crearás una variable local independiente con
el mismo nombre enmascarando la variable con el comportamiento mágico.

.. _tut-strings:

Cadenas de caracteres
---------------------

Además de números, Python puede manipular cadenas de texto, las cuales pueden
ser expresadas de distintas formas.  Pueden estar encerradas en comillas
simples o dobles::

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
formas.  Las líneas continuas se pueden usar, con una barra invertida como el
último carácter de la línea para indicar que la siguiente línea es la
continuación lógica de la línea::

   hola = "Esta es una larga cadena que contiene\n\
   varias líneas de texto, tal y como se hace en C.\n\
       Notar que los espacios en blanco al principio de la linea\
    son significantes."

   print hola

Notá que de todas formas se necesita embeber los salto de líneas con ``\n``;
la nueva línea que sigue a la barra invertida final es descartada.  Este
ejemplo imprimiría::

   Esta es una larga cadena que contiene
   varias líneas de texto, tal y como se hace en C.
        Notar que los espacios en blanco al principio de la linea son
        significantes.

Si se hace de la cadena de texto una cadena "cruda", la secuencia ``\n`` no
es convertida a salto de línea, pero la barra invertida al final de la línea
y el carácter de nueva línea en la fuente, ambos son incluidos en la cadena
como datos. Así, el ejemplo::

   hola = r"Esta es una larga cadena que contiene\n\
   varias líneas de texto, tal y como se hace en C."

   print hola

...imprimirá::

   Esta es una larga cadena que contiene\n\
   varias líneas de texto, tal y como se hace en C.

O, las cadenas de texto pueden ser rodeadas en un par de comillas triples:
``"""`` o ``'''``.  No se necesita escapar los finales de línea cuando se
utilizan comillas triples, pero serán incluidos en la cadena. ::

   print """
   Uso: algo [OPTIONS]
        -h                        Muestra el mensaje de uso
        -H nombrehost             Nombre del host al cual conectarse
   """

...produce la siguiente salida::

   Uso: algo [OPTIONS]
        -h                        Muestra el mensaje de uso
        -H nombrehost             Nombre del host al cual conectarse

El interprete imprime el resultado de operaciones entre cadenas de la misma
forma en que son tecleadas como entrada: dentro de comillas, y con comillas y
otros caracteres raros escapados con barras invertidas, para mostrar
el valor preciso.  La cadena de texto es encerrada con comillas dobles si
contiene una comilla simple y no comillas dobles, sino es encerrada con
comillas simples.  (La declaración :keyword:`print`, descrita luego,
puede ser usado para escribir cadenas sin comillas o escapes).

Las cadenas de texto pueden ser concatenadas (pegadas juntas) con el operador
``+`` y repetidas con ``*``::

   >>> palabra = 'Ayuda' + 'A'
   >>> palabra
   'AyudaA'
   >>> '<' + palabra*5 + '>'
   '<AyudaAAyudaAAyudaAAyudaAAyudaA>'

Dos cadenas de texto juntas son automáticamente concatenadas; la primer línea
del ejemplo anterior podría haber sido escrita ``palabra = 'Ayuda' 'A'``; esto
solo funciona con dos literales, no con expresiones arbitrarias::

   >>> 'cad' 'ena'                   #  <-  Esto es correcto
   'cadena'
   >>> 'cad'.strip() + 'ena'   #  <-  Esto es correcto
   'cadena'
   >>> 'cad'.strip() 'ena'     #  <-  Esto no es correcto
   Traceback (most recent call last):
   ...
   SyntaxError: invalid syntax

Las cadenas de texto se pueden indexar; como en C, el primer carácter de la
cadena tiene el índice 0.  No hay un tipo de dato para los caracteres; un
carácter es simplemente una cadena de longitud uno.  Como en Icon, se pueden
especificar subcadenas con la *notación de rebanadas*: dos índices separados
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

A diferencia de las cadenas de texto en C, en Python no pueden ser
modificadas.  Intentar asignar a una posición de la cadena es un error::

   >>> palabra[0] = 'x'
   Traceback (most recent call last):
   ...
   TypeError: 'str' object does not support item assignment
   >>> palabra[:1] = 'Mas'
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: 'str' object does not support item assignment

Sin embargo, crear una nueva cadena con contenido combinado es fácil y
eficiente::

   >>> 'x' + palabra[1:]
   'xyudaA'
   >>> 'Mas' + palabra[5]
   'MasA'

Algo útil de las operaciones de rebanada: ``s[:i] + s[i:]`` es ``s``.
::

   >>> palabra[:2] + palabra[2:]
   'AyudaA'
   >>> palabra[:3] + palabra[3:]
   'AyudaA'

Los índices degenerados en las rebanadas son manejados bien: un índice
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

   >>> palabra[-1]     # El último caracter
   'A'
   >>> palabra[-2]     # El penúltimo caracter
   'a'
   >>> palabra[-2:]    # Los últimos dos caracteres
   'aA'
   >>> palabra[:-2]    # Todo menos los últimos dos caracteres
   'Ayud'

Pero notá que -0 es en realidad lo mismo que 0, ¡por lo que no cuenta desde
la derecha! ::

   >>> palabra[-0]     # (ya que -0 es igual a 0)
   'A'

Los índices negativos fuera de rango son truncados, pero esto no funciona para
índices de un solo elemento (no rebanada)::

   >>> palabra[-100:]
   'AyudaA'
   >>> palabra[-10]    # error
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   IndexError: string index out of range

Una forma de recordar cómo funcionan las rebanadas es pensar en los índices
como puntos *entre* caracteres, con el punto a la izquierda del primer carácter
numerado en 0.  Luego, el punto a la derecha del último carácter de una cadena
de *n* caracteres tienen índice *n*, por ejemplo::

    +---+---+---+---+---+---+
    | A | y | u | d | a | A |
    +---+---+---+---+---+---+
    0   1   2   3   4   5   6
   -6  -5  -4  -3  -2  -1

La primer fila de números da la posición de los índices 0...6 en la cadena;
la segunda fila da los correspondientes índices negativos. La rebanada de *i*
a *j* consiste en todos los caracteres entre los puntos etiquetados *i* y *j*,
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
      Las cadenas de texto y la cadenas de texto Unicode descritas en la
      siguiente sección son ejemplos de *tipos secuencias*, y soportan
      las operaciones comunes para esos tipos.

   :ref:`string-methods`
      Tanto las cadenas de texto normales como las cadenas de texto Unicode
      soportan una gran cantidad de métodos para transformaciones básicas y
      búsqueda.

   :ref:`new-string-formatting`
      Aquí se da información sobre formateo de cadenas de texto con
      :meth:`str.format`.

   :ref:`string-formatting`
      Aquí se describe con más detalle las operaciones viejas para formateo
      usadas cuando una cadena de texto o una cadena Unicode están a la
      izquierda del operador ``%``.


.. _tut-unicodestrings:

Cadenas de texto Unicode
------------------------

.. sectionauthor:: Marc-Andre Lemburg <mal@lemburg.com>

Desde la versión 2.0 de Python, se encuentra disponible un nuevo tipo de datos
para que los programadores almacenen texto: el objeto Unicode. Puede ser usado
para almacenar y manipular datos Unicode (ver http://www.unicode.org/) y se
integran bien con los objetos existentes para cadenas de texto, mediante
auto-conversión cuando es necesario.

Unicode tiene la ventaja de tener un número ordinal para cada carácter
usado tanto en textos modernos como antiguos.  Previamente, había sólo
256 ordinales posibles para los caracteres en scripts.  Los textos
eran típicamente asociados a un código que relaciona los ordinales a caracteres
en scripts.  Esto lleva a mucha confusión, especialmente al internacionalizar
software.  Unicode resuelve estos problemas definiendo una sola codificación
para todos los scripts.

Crear cadenas Unicode en Python es tan simple como crear cadenas de texto
normales::

   >>> u'Hola Mundo!'
   u'Hola Mundo!'

La ``'u'`` al frente de la comilla indica que se espera una cadena Unicode. Si
querés incluir caracteres especiales en la cadena, podés hacerlo usando una
forma de escapar caracteres Unicode provista por Python.  El siguiente ejemplo
muestra cómo::

   >>> u'Hola\u0020Mundo!'
   u'Hola Mundo!'

La secuencia de escape ``\u0020`` indica que se debe insertar el carácter
Unicode con valor ordinal 0x0020 (el espacio en blanco) en la posición dada.

Otros caracteres son interpretados usando su respectivo valor ordinal como
ordinales Unicode. Si tenés cadenas de texto literales en la codificación
estándar Latin-1 que es muy usada en países occidentales, encontrarás
conveniente que los primeros 256 caracteres de Unicode son los mismos primeros
256 caracteres de Latin-1.

También existe un modo crudo para expertos, del mismo modo que con las cadenas
de texto normales. Debés anteponer 'ur' a la comilla inicial para que Python
use el modo de escape crudo de Unicode. Solo se aplicará la conversión
``\uXXXX`` si hay un número impar de barras invertidas frente a la 'u'. ::

   >>> ur'Hola\u0020Mundo!'
   u'Hola Mundo!'
   >>> ur'Hola\\u0020Mundo!'
   u'Hola\\\\u0020Mundo!'

El modo crudo es útil principalmente cuando tenés que insertar muchas
barras invertidas, como puede suceder al trabajar con expresiones regulares.

Además de estas codificaciones estándar, Python provee muchas más formas de
crear cadenas de texto Unicode en las bases de codificaciones conocidas.

.. index:: builtin: unicode

La función predefinida :func:`unicode` da acceso a todos los codecs
(CODificadores y DECodificadores).  Algunos de los códigos más conocidos
que estos codecs pueden convertir son *Latin-1*, *ASCII*, *UTF-8*, y *UTF-16*.
Los dos últimas son códigos de longitud variable que almacenan cada
carácter Unicode en uno o más bytes.  El código por defecto es normalmente
configurado a ASCII, que contiene los caracteres del rango 0-127 y rechaza
cualquier otro con un error.  Cuando una cadena Unicode se imprime, escribe en
un archivo, o se convierte con la función :func:`str`, se realiza la conversión
utilizando el código por defecto. ::

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

Para convertir una cadena Unicode en una cadena de 8-bit utilizando un
código en particular, los objetos Unicode tienen un método :func:`encode`
que toma un argumento, el nombre del código. Se prefieren los nombres
en minúsculas para los nombres de los códigos. ::

   >>> u"äöü".encode('utf-8')
   '\xc3\xa4\xc3\xb6\xc3\xbc'

Si tenés datos en un código en particular y querés producir la cadena
Unicode correspondiente, podés usar la función :func:`unicode` con el nombre
del código como segundo argumento. ::

   >>> unicode('\xc3\xa4\xc3\xb6\xc3\xbc', 'utf-8')
   u'\xe4\xf6\xfc'


.. _tut-lists:

Listas
------

Python tiene varios tipos de datos *compuestos*, usados para agrupar otros
valores.  El más versátil es la *lista*, la cual puede ser escrita como una
lista de valores separados por coma (ítems) entre corchetes.  No es necesario
que los ítems de una lista tengan todos el mismo tipo. ::

   >>> a = ['pan', 'huevos', 100, 1234]
   >>> a
   ['pan', 'huevos', 100, 1234]

Como los índices de las cadenas de texto, los índices de las listas comienzan
en 0, y las listas pueden ser rebanadas, concatenadas y todo lo demás::

   >>> a[0]
   'pan'
   >>> a[3]
   1234
   >>> a[-2]
   100
   >>> a[1:-1]
   ['huevos', 100]
   >>> a[:2] + ['carne', 2*2]
   ['pan', 'huevos', 'carne', 4]
   >>> 3*a[:3] + ['Boo!']
   ['pan', 'huevos', 100, 'pan', 'huevos', 100, 'pan', 'huevos', 100, 'Boo!']

A diferencia de las cadenas de texto, que son *inmutables*, es posible cambiar
un elemento individual de una lista::

   >>> a
   ['pan', 'huevos', 100, 1234]
   >>> a[2] = a[2] + 23
   >>> a
   ['pan', 'huevos', 123, 1234]

También es posible asignar a una rebanada, y esto incluso puede cambiar la
longitud de la lista o vaciarla totalmente::

   >>> # Reemplazar algunos elementos:
   ... a[0:2] = [1, 12]
   >>> a
   [1, 12, 123, 1234]
   >>> # Borrar algunos:
   ... a[0:2] = []
   >>> a
   [123, 1234]
   >>> # Insertar algunos:
   ... a[1:1] = ['bruja', 'xyzzy']
   >>> a
   [123, 'bruja', 'xyzzy', 1234]
   >>> # Insertar (una copia de) la misma lista al principio
   >>> a[:0] = a
   >>> a
   [123, 'bruja', 'xyzzy', 1234, 123, 'bruja', 'xyzzy', 1234]
   >>> # Vaciar la lista: reemplazar todos los items con una lista vacía
   >>> a[:] = []
   >>> a
   []

La función predefinida :func:`len` también sirve para las listas:

   >>> a = ['a', 'b', 'c', 'd']
   >>> len(a)
   4

Es posible anidar listas (crear listas que contengan otras listas), por
ejemplo::

   >>> q = [2, 3]
   >>> p = [1, q, 4]
   >>> len(p)
   3
   >>> p[1]
   [2, 3]
   >>> p[1][0]
   2
   >>> p[1].append('extra')     # Ver seccion 5.1
   >>> p
   [1, [2, 3, 'extra'], 4]
   >>> q
   [2, 3, 'extra']

Notá que en el último ejemplo, ``p[1]`` y ``q`` ¡realmente hacen referencia
al mismo objeto!  Volveremos a la *semántica de los objetos* más adelante.


.. _tut-firststeps:

Primeros pasos hacia la programación
====================================

Por supuesto, podemos usar Python para tareas más complicadas que sumar dos
y dos.  Por ejemplo, podemos escribir una subsecuencia inicial de la serie de
*Fibonacci* así::

   >>> # Series de Fibonacci:
   ... # la suma de dos elementos define el siguiente
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

Este ejemplo introduce varias características nuevas.

* La primer línea contiene una *asignación múltiple*: las variables``a`` y
  ``b`` toman en forma simultanea los nuevos valores 0 y 1.  En la última linea
  esto es vuelto a usar, demostrando que las expresiones a la derecha son
  evaluadas antes de que suceda cualquier asignación.  Las expresiones a la
  derecha son evaluadas de izquierda a derecha.

* El bucle :keyword:`while` se ejecuta mientras la condición (aquí: ``b < 10``)
  sea verdadera.  En Python, como en C, cualquier entero distinto de cero es
  verdadero; cero es falso.  La condición también puede ser una cadena de texto
  o una lista, de hecho cualquier secuencia; cualquier cosa con longitud
  distinta de cero es verdadero, las secuencias vacías son falsas.  La prueba
  usada en el ejemplo es una comparación simple.  Los operadores estándar de
  comparación se escriben igual que en C: ``<`` (menor qué), ``>`` (mayor qué),
  ``==`` (igual a), ``<=`` (menor o igual qué), ``>=`` (mayor o igual qué) y
  ``!=`` (distinto a).

* El *cuerpo* del bucle está *sangrado*: la sangría es la forma que usa
  Python para agrupar declaraciones.  El intérprete interactivo de Python
  (¡aún!) no provee una facilidad inteligente para editar líneas, así que
  debés teclear un tab o espacio(s) para cada línea sangrada.  En la práctica
  vas a preparar entradas más complicadas para Python con un editor de
  texto; la mayoría de los editores de texto tienen la facilidad de
  agregar la sangría automáticamente.  Al ingresar una declaración compuesta en
  forma interactiva, debés finalizar con una línea en blanco para indicar que
  está completa (ya que el analizador no puede adivinar cuando tecleaste la
  última línea).  Notá que cada línea de un bloque básico debe estar sangrada
  de la misma forma.

* La declaración :keyword:`print` escribe el valor de la o las expresiones que
  se le pasan.  Difiere de simplemente escribir la expresión que se quiere
  mostrar (como hicimos antes en los ejemplos de la calculadora) en la forma
  en que maneja múltiples expresiones y cadenas.  Las cadenas de texto son
  impresas sin comillas, y un espacio en blanco es insertado entre los
  elementos, así podés formatear cosas de una forma agradable::

     >>> i = 256*256
     >>> print 'El valor de i es', i
     El valor de i es 65536

  Una coma final evita el salto de línea al final de la salida::

     >>> a, b = 0, 1
     >>> while b < 1000:
     ...     print b,
     ...     a, b = b, a+b
     ...
     1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987

  Notá que el intérprete inserta un salto de línea antes de imprimir el
  próximo prompt si la última línea no estaba completa.
