.. _tut-fp-issues:

******************************************************
Aritmética de Punto Flotante: Problemas y Limitaciones
******************************************************

.. sectionauthor:: Tim Peters <tim_one@users.sourceforge.net>


Los números de punto flotante se representan en el hardware de la
computadora en fracciones en base 2 (binario).  Por ejemplo, la fracción
decimal ::

   0.125

...tiene el valor 1/10 + 2/100 + 5/1000, y de la misma manera la fracción
binaria ::

   0.001

...tiene el valor 0/2 + 0/4 + 1/8.  Estas dos fracciones tienen valores
idénticos, la única diferencia real es que la primera está escrita en
notación fraccional en base 10 y la segunda en base 2.

Desafortunadamente, la mayoría de las fracciones decimales no pueden
representarse exactamente como fracciones binarias.  Como consecuencia, en
general los números de punto flotante decimal que ingresás en la computadora
son sólo aproximados por los números de punto flotante binario que realmente
se guardan en la máquina.

El problema es más fácil de entender primero en base 10.  Considerá la
fracción 1/3.  Podés aproximarla como una fracción de base 10 ::

   0.3

...o, mejor, ::


   0.33

...o, mejor, ::

   0.333

...y así.  No importa cuantos dígitos desees escribir, el resultado nunca será
exactamente 1/3, pero será una aproximación cada vez mejor de 1/3.

De la misma manera, no importa cuantos dígitos en base 2 quieras usar, el
valor decimal 0.1 no puede representarse exactamente como una fracción en
base 2.  En base 2, 1/10 es la siguiente fracción que se repite
infinitamente::

   0.0001100110011001100110011001100110011001100110011...

Frená en cualquier número finito de bits, y tendrás una aproximación.  Es
por esto que ves cosas como::

   >>> 0.1
   0.10000000000000001

En la mayoría de las máquinas de hoy en día, eso es lo que verás si ingresás
0.1 en un prompt de Python.  Quizás no, sin embargo, porque la cantidad de
bits usados por el hardware para almacenar valores de punto flotante puede
variar en las distintas máquinas, y Python sólo muestra una aproximación del
valor decimal verdadero de la aproximación binaria guardada por la máquina.
En la mayoría de las máquinas, si Python fuera a mostrar el verdadero valor
decimal de la aproximación almacenada por 0.1, tendría que mostrar sin
embargo ::

   >>> 0.1
   0.1000000000000000055511151231257827021181583404541015625

El prompt de Python usa la función integrada :func:`repr` para obtener una
versión en cadena de caracteres de todo lo que muestra.  Para flotantes,
``repr(float)`` redondea el valor decimal verdadero a 17 dígitos
significativos, dando ::

   0.10000000000000001

``repr(float)`` produce 17 dígitos significativos porque esto es suficiente
(en la mayoría de las máquinas) para que se cumpla ``eval(repr(x)) == x``
exactamente para todos los flotantes finitos *X*, pero redondeando a 16
dígitos no es suficiente para que sea verdadero.

Notá que esta es la verdadera naturaleza del punto flotante binario: no es
un error de Python, y tampoco es un error en tu código.  Verás lo mismo en todos
los lenguajes que soportan la aritmética de punto flotante de tu hardware (a
pesar de que en algunos lenguajes por omisión no *muestren* la diferencia, o
no lo hagan en todos los modos de salida).

La función integrada :func: `str` de Python produce sólo 12 dígitos
significativos, y quizás quieras usar esa.  Normalmente ``eval(str(x))`` no
reproducirá `x`, pero la salida quizás sea más placentera de ver::

   >>> print str(0.1)
   0.1

Es importante darse cuenta de que esto es, realmente, una ilusión: el valor
en la máquina no es exactamente 1/10, simplemente estás redondeando el valor
que se *muestra* del valor verdadero de la máquina.

A esta se siguen otras sorpresas.  Por ejemplo, luego de ver::

   >>> 0.1
   0.10000000000000001

...quizás estés tentado de usar la función :func:`round` para recortar el
resultado al dígito que esperabas.  Pero es lo mismo::

   >>> round(0.1, 1)
   0.10000000000000001

El problema es que el valor de punto flotante binario almacenado para "0.1"
ya era la mejor aproximación binaria posible de 1/10, de manera que intentar
redondearla nuevamente no puede mejorarla: ya era la mejor posible.

Otra consecuencia es que como 0.1 no es exactamente 1/10, sumar diez valores
de 0.1 quizás tampoco dé exactamente 1.0::

   >>> suma = 0.0
   >>> for i in range(10):
   ...     suma += 0.1
   ...
   >>> suma
   0.99999999999999989

La aritmética de punto flotante binaria tiene varias sorpresas como esta.
El problema con "0.1" es explicado con detalle abajo, en la sección "Error
de Representación".  Mirá los Peligros del Punto Flotante (en inglés,
`The Perils of Floating Point <http://www.lahey.com/float.htm>`_) para una
más completa recopilación de otras sorpresas normales.

Como dice cerca del final, "no hay respuestas fáciles".  A pesar de eso,
¡no le tengas mucho miedo al punto flotante!  Los errores en las operaciones
flotantes de Python se heredan del hardware de punto flotante, y en la
mayoría de las máquinas están en el orden de no más de una 1 parte en
2\*\*53 por operación.  Eso es más que adecuado para la mayoría de las
tareas, pero necesitás tener en cuenta que no es aritmética decimal, y que
cada operación de punto flotante sufre un nuevo error de redondeo.

A pesar de que existen casos patológicos, para la mayoría de usos casuales
de la aritmética de punto flotante al final verás el resultado que esperás
si simplemente redondeás lo que mostrás de tus resultados finales al número
de dígitos decimales que esperás.  :func:`str` es normalmente suficiente, y
para un control más fino mirá los parámetros del método de formateo
:meth:`str.format` en :ref:`formatstrings`.


.. _tut-fp-error:

Error de Representación
=======================

Esta sección explica el ejemplo "0.1" en detalle, y muestra como en la
mayoría de los casos vos mismo podés realizar un análisis exacto como este.
Se asume un conocimiento básico de la representación de punto flotante
binario.

:dfn:`Error de representación` se refiere al hecho de que algunas (la
mayoría) de las fracciones decimales no pueden representarse exactamente
como fracciones binarias (en base 2).  Esta es la razón principal de por qué
Python (o Perl, C, C++, Java, Fortran, y tantos otros) frecuentemente no
mostrarán el número decimal exacto que esperás::

   >>> 0.1
   0.10000000000000001

¿Por qué es eso?  1/10 no es representable exactamente como una fracción
binaria.  Casi todas las máquinas de hoy en día (Noviembre del 2000) usan
aritmética de punto flotante IEEE-754, y casi todas las plataformas mapean
los flotantes de Python al "doble precisión" de IEEE-754.  Estos "dobles"
tienen 53 bits de precisión, por lo tanto en la entrada la computadora
intenta convertir 0.1 a la fracción más cercana que puede de la forma
*J*/2\*\**N* donde *J* es un entero que contiene exactamente 53 bits.
Reescribiendo ::

   1 / 10 ~= J / (2**N)

...como ::

   J ~= 2**N / 10

...y recordando que *J* tiene exactamente 53 bits (es ``>= 2**52`` pero
``< 2**53``), el mejor valor para *N* es 56::

   >>> 2**52
   4503599627370496L
   >>> 2**53
   9007199254740992L
   >>> 2**56/10
   7205759403792793L

O sea, 56 es el único valor para *N* que deja *J* con exactamente 53 bits.
El mejor valor posible para *J* es entonces el cociente redondeado::

   >>> q, r = divmod(2**56, 10)
   >>> r
   6L

Ya que el resto es más que la mitad de 10, la mejor aproximación se obtiene
redondeándolo::

   >>> q+1
   7205759403792794L

Por lo tanto la mejor aproximación a 1/10 en doble precisión 754 es eso
sobre 2\*\*56, o ::

   7205759403792794 / 72057594037927936

Notá que como lo redondeamos, esto es un poquito más grande que 1/10; si no
lo hubiéramos redondeado, el cociente hubiese sido un poquito menor que
1/10.  ¡Pero no hay caso en que sea *exactamente* 1/10!

Entonces la computadora nunca "ve" 1/10:  lo que ve es la fracción exacta de
arriba, la mejor aproximación al flotante doble de 754 que puede obtener::

   >>> .1 * 2**56
   7205759403792794.0

Si multiplicamos esa fracción por 10\*\*30, podemos ver el valor (truncado)
de sus 30 dígitos más significativos::

   >>> 7205759403792794 * 10**30 / 2**56
   100000000000000005551115123125L

...lo que significa que el valor exacto almacenado en la computadora es
aproximadamente igual al valor decimal 0.100000000000000005551115123125.
Redondeando eso a 17 dígitos significativos da el 0.10000000000000001 que
Python muestra (bueno, mostraría en cualquier plataforma que cumpla con 754
cuya biblioteca en C haga la mejor conversión posible en entrada y
salida... ¡la tuya quizás no!).
