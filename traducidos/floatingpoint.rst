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

Frená en cualquier número finito de bits, y tendrás una aproximación.  En
la mayoría de las máquinas hoy en día, los float se aproximan usando una
fracción binaria con el numerador usando los primeros 53 bits con el bit
más significativos y el denominador como una potencia de dos.  En el caso de
1/10, la fracción binaria es ``3602879701896397 / 2 ** 55`` que está cerca
pero no es exactamente el valor verdadero de 1/10.

La mayoría de los usuarios no son conscientes de esta aproximación por la
forma en que se muestran los valores.  Python solamente muestra una
aproximación decimal al valor verdadero decimal de la aproximación binaria
almacenada por la máquina.  En la mayoría de las máquinas, si Python fuera
a imprimir el verdadero valor decimal de la aproximación binaria almacenada
para 0.1, debería mostrar ::

   >>> 0.1
   0.1000000000000000055511151231257827021181583404541015625

Esos son más dígitos que lo que la mayoría de la gente encuentra útil, por
lo que Python mantiene manejable la cantidad de dígitos al mostrar en su
lugar un valor redondeado ::

   >>> 1 / 10
   0.1

Sólo recordá que, a pesar de que el valor mostrado resulta ser exactamente
1/10, el valor almacenado realmente es la fracción binaria más cercana
posible.

Interesantemente, hay varios números decimales que comparten la misma
fracción binaria más aproximada. Por ejemplo, los números ``0.1``,
``0.10000000000000001`` y
``0.1000000000000000055511151231257827021181583404541015625`` son todos
aproximados por ``3602879701896397 / 2 ** 55``.  Ya que todos estos valores
decimales comparten la misma aproximación, se podría mostrar cualquiera de
ellos para preservar el invariante ``eval(repr(x)) == x``.

Históricamente, el prompt de Python y la función integrada :func:`repr`
eligieron el valor con los 17 dígitos, ``0.10000000000000001``.  Desde
Python 3.1, en la mayoría de los sistemas Python ahora es capaz de elegir
la forma más corta de ellos y mostrar ``0.1``.

Notá que esta es la verdadera naturaleza del punto flotante binario: no es
un error de Python, y tampoco es un error en tu código.  Verás lo mismo
en todos los lenguajes que soportan la aritmética de punto flotante de
tu hardware (a pesar de que en algunos lenguajes por omisión no
*muestren* la diferencia, o no lo hagan en todos los modos de salida).

Para una salida más elegante, quizás quieras usar el formateo de cadenas
de texto para generar un número limitado de dígitos significativos::

   >>> format(math.pi, '.12g')  # da 12 dígitos significativos
   '3.14159265359'

   >>> format(math.pi, '.2f')   # da 2 dígitos luego del punto
   '3.14'

   >>> repr(math.pi)
   '3.141592653589793'

Es importante darse cuenta que esto es, realmente, una ilusión: estás
simplemente redondeando al *mostrar* el valor verdadero de la máquina.

Una ilusión puede generar otra.  Por ejemplo, ya que 0.1 no es exactamente
1/10, sumar tres veces 0.1 podría también no generar exactamente 0.3::

   >>> .1 + .1 + .1 == .3
   False

También, ya que 0.1 no puede acercarse más al valor exacto de 1/10 y
0.3 no puede acercarse más al valor exacto de 3/10, redondear primero
con la función :func:`round` no puede ayudar::

   >>> round(.1, 1) + round(.1, 1) + round(.1, 1) == round(.3, 1)
   False

A pesar que los números no pueden acercarse a los valores exactos que
pretendemos, la función :func:`round` puede ser útil para redondear
a posteriori, para que los resultados con valores inexactos se puedan
comparar entre sí::

    >>> round(.1 + .1 + .1, 10) == round(.3, 10)
    True

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
:meth:`str.format` en :ref:`string-formatting`.

Para los casos de uso que necesitan una representación decimal exacta,
probá el módulo :mod:`decimal`, que implementa aritmética decimal útil
para aplicaciones de contabilidad y de alta precisión.

El módulo :mod:`fractions` soporta otra forma de aritmética exacta, ya que
implementa aritmética basada en números racionales (por lo que números como
1/3 pueden ser representados exactamente).

Si sos un usuario frecuente de las operaciones de punto flotante deberías
pegarle una mirada al paquete Numerical Python y otros paquetes para
operaciones matemáticas y estadísticas provistos por el proyecto
SciPy. Mirá <http://scipy.org>.

Python provee herramientas que pueden ayudar en esas raras ocasiones
cuando realmente *querés* saber el valor exacto de un float. El método
:meth:`float.as_integer_ratio` expresa el valor del float como una
fracción::

   >>> x = 3.14159
   >>> x.as_integer_ratio()
   (3537115888337719, 1125899906842624)

Ya que la fracción es exacta, se puede usar para recrear sin pérdidas
el valor original::

    >>> x == 3537115888337719 / 1125899906842624
    True

El método :meth:`float.hex` expresa un float en hexadecimal (base 16),
nuevamente devolviendo el valor exacto almacenado por tu computadora::

   >>> x.hex()
   '0x1.921f9f01b866ep+1'

Esta representación hexadecimal precisa se puede usar para reconstruir
el valor exacto del float::

    >>> x == float.fromhex('0x1.921f9f01b866ep+1')
    True

Ya que la representación es exacta, es útil para portar valores a través
de diferentes versiones de Python de manera confiable (independencia de
plataformas) e intercambiar datos con otros lenguajes que soportan el
mismo formato (como Java y C99).

Otra herramienta útil es la función :func:`math.fsum` que ayuda a mitigar
la pérdida de precisión durante la suma.  Esta función lleva la cuenta de
"dígitos perdidos" mientras se suman los valores en un total.  Eso puede
hacer una diferencia en la exactitud de lo que se va sumando para que los
errores no se acumulen al punto en que afecten el total final::

   >>> sum([0.1] * 10) == 1.0
   False
   >>> math.fsum([0.1] * 10) == 1.0
   True


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
mostrarán el número decimal exacto que esperás.

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

    >>> 2**52 <=  2**56 // 10  < 2**53
    True

O sea, 56 es el único valor para *N* que deja *J* con exactamente 53 bits.
El mejor valor posible para *J* es entonces el cociente redondeado::

   >>> q, r = divmod(2**56, 10)
   >>> r
   6

Ya que el resto es más que la mitad de 10, la mejor aproximación se obtiene
redondeándolo::

   >>> q+1
   7205759403792794

Por lo tanto la mejor aproximación a 1/10 en doble precisión 754 es::

   7205759403792794 / 2 ** 56

El dividir tanto el numerador como el denominador reduce la fracción a::

   3602879701896397 / 2 ** 55

Notá que como lo redondeamos, esto es un poquito más grande que 1/10; si no
lo hubiéramos redondeado, el cociente hubiese sido un poquito menor que
1/10.  ¡Pero no hay caso en que sea *exactamente* 1/10!

Entonces la computadora nunca "ve" 1/10:  lo que ve es la fracción exacta de
arriba, la mejor aproximación al flotante doble de 754 que puede obtener::

   >>> 0.1 * 2 ** 55
   3602879701896397.0

Si multiplicamos esa fracción por 10\*\*55, podemos ver el valor hasta los
55 dígitos decimales::

   >>> 3602879701896397 * 10 ** 55 // 2 ** 55
   1000000000000000055511151231257827021181583404541015625

...lo que significa que el valor exacto almacenado en la computadora es igual
al valor decimal 0.1000000000000000055511151231257827021181583404541015625.
En lugar de mostrar el valor decimal completo, muchos lenguajes (incluyendo
versiones más viejas de Python), redondean el resultado a 17 dígitos
significativos::

   >>> format(0.1, '.17f')
   '0.10000000000000001'

Los módulos :mod:`fractions` y :mod:`decimal` hacen fácil estos cálculos::

   >>> from decimal import Decimal
   >>> from fractions import Fraction

   >>> Fraction.from_float(0.1)
   Fraction(3602879701896397, 36028797018963968)

   >>> (0.1).as_integer_ratio()
   (3602879701896397, 36028797018963968)

   >>> Decimal.from_float(0.1)
   Decimal('0.1000000000000000055511151231257827021181583404541015625')

   >>> format(Decimal.from_float(0.1), '.17')
   '0.10000000000000001'
