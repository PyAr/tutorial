.. _tut-classes:

******
Clases
******

El mecanismo de clases de Python agrega clases al lenguaje con un mínimo de
nuevas sintáxis y semánticas.  Es una mezcla de los mecanismos de clase
encontrados en C++ y Modula-3.  Como es cierto para los módulos, las clases en
Python no ponen una barrera absoluta entre la definición y el usuario, sino que
más bien se apoya en la cortesía del usuario de no "forzar la definición".  Sin
embargo, se mantiene el poder completo de las características más importantes
de las clases: el mecanismo de la herencia de clases permite múltiples clases
base, una clase derivada puede sobreescribir cualquier método de su(s) clase(s)
base, y un método puede llamar al método de la clase base con el mismo nombre.
Los objetos pueden tener una cantidad arbitraria de datos privados.

En terminología de C++, todos los miembros de las clases (incluyendo los
miembros de datos), son *públicos*, y todas las funciones miembro son
*virtuales*.  No hay constructores o destructores especiales.  Como en
Modula-3, no hay atajos para hacer referencia a los miembros del objeto desde
sus métodos: la función método se declara con un primer argumento explícito que
representa al objeto, el cual se provee implícitamente por la llamada.  Como
en Smalltalk, las clases mismas son objetos, aunque en un más amplio sentido
de la palabra: en Python, todos los tipos de datos son objetos.  Esto provee
una semántica para importar y renombrar.  A diferencia de C++ y Modula-3, los
tipos de datos integrados pueden usarse como clases base para que el usuario
los extienda.  También, como en C++ pero a diferencia de Modula-3, la mayoría
de los operadores integrados con sintáxis especial (operadores aritméticos, de
subíndice, etc.) pueden ser redefinidos por instancias de la clase.


.. _tut-terminology:

Unas palabras sobre terminología
================================

Sin haber una terminología universalmente aceptada sobre clases, haré uso
ocasional de términos de Smalltalk y C++.  (Usaría términos de Modula-3, ya que
su semántica orientada a objetos es más cercanas a Python que C++, pero no
espero que muchos lectores hayan escuchado hablar de él).

Los objetos tienen individualidad, y múltiples nombres (en muchos ámbitos)
pueden vincularse al mismo objeto.  Esto se conoce como *aliasing* en otros
lenguajes.  Normalmente no se aprecia esto a primera vista en Python, y puede
ignorarse sin problemas cuando se maneja tipos básicos inmutables (números,
cadenas, tuplas).  Sin embargo, el *aliasing*, o renombrado,  tiene un efecto
(intencional!) sobre la semántica de código Python que involucra objetos
mutables como listas, diccionarios, y la mayoría de tipos que representan
entidades afuera del programa (archivos, ventanas, etc.).  Esto se usa
normalmente para beneficio del programa, ya que los renombres funcionan como
punteros en algunos aspectos.  Por ejemplo, pasar un objeto es barato ya que
la implementación solamente pasa el puntero; y si una función modifica el
objeto que fue pasado, el que la llama verá el cambio; esto elimina la
necesidad de tener dos formas diferentes de pasar argumentos, como en Pascal.


.. _tut-scopes:


Alcances y espacios de nombres en Python
========================================

Antes de ver clases, primero debo decirte algo acerca de las reglas de alcance
de Python.  Las definiciones de clases hacen unos lindos trucos con los
espacios de nombres, y necesitás saber cómo funcionan los alcances y espacios
de nombres para entender por completo cómo es la cosa.
De paso, los conocimientos en este tema son útiles para cualquier programador
Python avanzado.

Comenzemos con unas definiciones.

Un *espacio de nombres* es un mapeo de nombres a objetos.  Muchos espacios de
nombres están implementados en este momento como diccionarios de Python, pero
eso no se nota para nada (excepto por el desempeño), y puede cambiar en el
futuro.  Como ejemplos de espacios de nombres tenés: el conjunto de nombres
incluídos (funciones como :func:`abs`, y los nombres de excepciones
integradas); los nombres globales en un módulo; y los nombres locales en la
invocación a una función.  Lo que es importante saber de los espacios de
nombres es que no hay relación en absoluto entre los nombres de espacios de
nombres distintos; por ejemplo, dos módulos diferentes pueden tener definidos
los dos una función "maximizar" sin confusión -- los usuarios de los módulos
deben usar el nombre del módulo como prefijo.

Por cierto, yo uso la palabra *atributo* para cualquier cosa después de un
punto --- por ejemplo, en la expresión ``z.real``, ``real`` es un atributo del
objeto ``z``. Estrictamente hablando, las referencias a nombres en módulos son
referencias a atributos: en la expresión ``modulo.funcion``, ``modulo`` es un
objeto módulo y ``funcion`` es un atributo de éste. En este caso hay un mapeo
directo entre los atributos del módulo y los nombres globales definidos en el
módulo: ¡están compartiendo el mismo espacio de nombres! [#]_

Los atributos pueden ser de sólo lectura, o de escritura.  En el último caso es
posible la asignación a atributos.  Los atributos de módulo pueden escribirse:
podés escribir ``modulo.la_respuesta = 42``.  Los atributos de escritura se
pueden borrar también con la instrucción :keyword:`del`.  Por ejemplo,
``del modulo.la_respuesta`` va a eliminar el atributo :attr:`the_answer` del
objeto con nombre ``modulo``.

Los espacios de nombres se crean en diferentes momentos y con diferentes
tiempos de vida.  El espacio de nombres que contiene los nombres incluidos se
crea cuando se inicia el intérprete, y nunca se borra.  El espacio de nombres
global de un módulo se crea cuando se lee la definición de un módulo;
normalmente, los espacios de nombres de módulos también duran hasta que el
intérprete finaliza.  Las instrucciones ejecutadas en el nivel de llamadas
superior del intérprete, ya sea desde un script o interactivamente, se
consideran parte del módulo llamado :mod:`__main__`, por lo tanto tienen su
propio espacio de nombres global.  (Los nombres incluídos en realidad también
viven en un módulo; este se llama :mod:`__builtin__`.)

El espacio de nombres local a una función se crea cuando la función es llamada,
y se elimina cuando la función retorna o lanza una excepción que no se maneje
dentro de la función.  (Podríamos decir que lo que pasa en realidad es que ese
espacio de nombres se "olvida".)  Por supuesto, las llamadas recursivas tienen
cada una su propio espacio de nombres local.

Un *alcance* es una región textual de un programa en Python donde un espacio de
nombres es accesible directamente.  "Accesible directamente" significa que una
referencia sin calificar a un nombre intenta encontrar dicho nombre dentro del
espacio de nombres.

Aunque los alcances se determinan estáticamente, se usan dinámicamente. En
cualquier momento durante la ejecución hay por lo menos tres alcances anidados
cuyos espacios de nombres son directamente accesibles: el ámbito interno, donde
se busca primero, contiene los nombres locales; los espacios de nombres de las
funciones anexas, en las cuales se busca empezando por el alcance adjunto más
cercano; el alcance intermedio, donde se busca a continuación, contiene el
módulo de nombres globales actual; y el alcance exterior (donde se busca al
final) es el espacio de nombres que contiene los nombres incluidos.

Si un nombre se declara como global, entonces todas las referencias y
asignaciones al mismo van directo al alcance intermedio que contiene los
nombres globales del módulo.  De otra manera, todas las variables que se
encuentren fuera del alcance interno son de sólo escritura (un intento de
escribir a esas variables simplemente crea una *nueva* variable en el alcance
interno, dejando intacta la variable externa del mismo nombre).

.. XXX mencionar nonlocal

Habitualmente, el alcance local referencia los nombres locales de la función
actual.  Fuera de una función, el alcance local referncia al mismo espacio de
nombres que el alcance global: el espacio de nombres del módulo. Las
definiciones de clases crean un espacio de nombres más en el alcance local.

Es importante notar que los alcances se determinan textualmente: el alcance
global de una función definida en un módulo es el espacio de nombres de ese
módulo, no importa desde dónde o con qué alias se llame a la función.  Por otro
lado, la búsqueda de nombres se hace dinámicamente, en tiempo de ejecución ---
sin embargo, la definición del lenguaje está evolucionando a hacer resolución
de nombres estáticamente, en tiempo de "compilación", ¡así que no te confíes de
la resolución de nombres dinámica! (De hecho, las variables locales ya se
determinan estáticamente.)

Una peculiaridad especial de Python es que -- si no hay una declaración
:keyword:`global` o :keyword:`nonlocal` en efecto -- las asignaciones a nombres
siempre van al alcance interno.  Las asignaciones no copian datos --- solamente
asocian nombres a objetos.  Lo mismo cuando se borra: la instrucción ``del x``
quita la asociación de ``x`` del espacio de nombres referenciado por el alcance
local.  De hecho, todas las operaciones que introducen nuevos nombres usan el
alcance local: en particular, las instrucciones import y las definiciones de
funciones asocian el módulo o nombre de la función al espacio de nombres en el
alcance local.  (La instrucción :keyword:`global` puede usarse para indicar
que ciertas variables viven en el alcance global.) 


.. _tut-firstclasses:

Un primer vistazo a las clases
==============================

Las clases introducen un poquito de sintaxis nueva, tres nuevos tipos de
objetos y algo de semántica nueva.


.. _tut-classdefinition:

Sintaxis de definición de clases
--------------------------------

La forma más sencilla de definición de clase se ve así::

   class Clase:
       <declaración-1>
       .
       .
       .
       <declaración-N>

Las definiciones de clases, al igual que las definiciones de funciones
(instrucciones :keyword:`def`) deben ejecutarse antes de que tengan efecto
alguno.  (Es concebible poner una definición de clase dentro de una rama de un
:keyword:`if`, o dentro de una función.)

En la práctica, las declaraciones dentro de una clase son definiciones de
funciones, pero otras declaraciones son permitidas, y a veces resultan útiles
--- veremos esto más adelante.  Las definiciones de funciones dentro de una
clase normalmente tienen una lista de argumentos peculiar, dictada por las
convenciones de invocación de métodos --- a esto también lo vemos más adelante.

Cuando se ingresa una definición de clase, se crea un nuevo espacio de nombres,
el cual se usa como alcance local --- por lo tanto, todas las asignaciones a
variables locales van a este nuevo espacio de nombres.  En particular, las
definiciones de funciones asocian el nombre de las funciones nuevas allí.

Cuando una definición de clase se finaliza normalmente se crea un
*objeto clase*. Básicamente, este objeto envuelve los contenidos del espacio
de nombres creado por la definición de la clase; aprenderemos más acerca de los
objetos clase en la sección siguiente.  El alcance local original (el que tenía
efecto justo antes de que ingrese la definición de la clase) es reinstaurado, y
el objeto clase se asocia allí al nombre que se le puso a la clase en el
encabezado de su definición (:class:`Clase` en el ejemplo).

.. _tut-classobjects:

Objetos clase
-------------

Los objetos clase soportan dos tipos de operaciones: referenciar atributos e
instanciación.

Para *referenciar atributos* se usa la sintaxis estándar de todas las
referencias a atributos en Python: ``objeto.nombre``.  Los nombres de atributo
válidos son todos los nombres que estaban en el espacio de nombres de la clase
cuando ésta se creó.  Por lo tanto, si la definición de la clase es así::

   class MiClase:
       "Simple clase de ejemplo"
       i = 12345
       def f(self):
           return 'hola mundo'

entonces ``MiClase.i`` y ``MiClase.f`` son referencias de atributos válidas,
que devuelven un entero y un objeto función respectivamente. Los atributos de
clase también pueden ser asignados, o sea que podés cambiar el valor de
``MiClase.i`` mediante asignación.
:attr:`__doc__` también es un atributo válido, que devuelve la documentación
que asociada a la clase: ``"Simple clase de ejemplo"``.

La *instanciación* de clases usa la notación de funciones.  Hacé de cuenta que
el objeto de clase es una función sin parámetros que devuelve una nueva
instancia de la clase.
Por ejemplo (para la clase de más arriba)::

   x = MiClase()

crea una nueva *instancia* de la clase y asigna este objeto a la variable local
``x``.

La operación de instanciación ("llamar" a un objeto clase) crea un objeto
vacío. Muchas clases necesitan crear objetos con instancias en un estado
inicial particular. Por lo tanto una clase puede definir un método especial
llamado :meth:`__init__`, de esta forma::

   def __init__(self):
       self.datos = []

Cuando una clase define un método :meth:`__init__`, la instanciación de la
clase automáticamente invoca a :meth:`__init__` para la instancia recién
creada.  Entonces, en este ejemplo, una instancia nueva e inicializada se puede
obtener haciendo::

   x = MiClase()

Por supuesto, el método :meth:`__init__` puede tener argumentos para mayor
flexibilidad.  En ese caso, los argumentos que se pasen al operador de
instanciación de la clase van a parar al método :meth:`__init__`.  Por
ejemplo, ::

   >>> class Complejo:
   ...     def __init__(self, partereal, parteimaginaria):
   ...         self.r = partereal
   ...         self.i = parteimaginaria
   ...
   >>> x = Complejo(3.0, -4.5)
   >>> x.r, x.i
   (3.0, -4.5)


.. _tut-instanceobjects:

Objetos Instancia
-----------------

Ahora, ¿Qué podemos hacer con los objetos instancia?  La única operación que
es entendida por los objetos instancia es la referencia de atributos.  Hay dos
tipos de nombres de atributos válidos, atributos de datos y métodos.

Los *atributos de datos* se corresponden con las "variables de instancia" en
Smalltalk, y con las "variables miembro" en C++.  Los atributos de datos no
necesitan ser declarados; tal como las variables locales son creados la primera
vez que se les asigna algo.  Por ejemplo, si ``x`` es la instancia de
:class:`MiClase` creada más arriba, el siguiente pedazo de código va a
imprimir el valor ``16``, sin dejar ningún rastro::

   x.contador = 1
   while x.contador < 10:
       x.contador = x.contador * 2
   print x.contador
   del x.contador

El otro tipo de referenciar atributos de instancia es el *método*.  Un método es
una función que "pertenece a" un objeto.  (En Python, el término método no está
limitado a instancias de clase: otros tipos de objetos pueden tener métodos también.
Por ejemplo, los objetos lista tienen métodos llamados append, insert, remove, sort,
y así sucesivamente.  Pero, en la siguiente explicación, usaremos el término método
para referirnos exclusivamente a métodos de objetos instancia de clase, a menos
que se especifique explícitamente lo contrario).

.. index:: object: method

Los nombres válidos de métodos de un objeto instancia dependen de su clase.
Por definición, todos los atributos de clase que son objetos funciones definen
metodos correspondientes de sus instancias.  Entonces, en nuestro ejemplo, ``x.f``
es una referencia a un método válido, dado que ``MiClase.f`` es una función, pero
``x.i`` no lo es, dado que ``MiClase.i`` no lo es. Pero ``x.f`` no es la misma
cosa que ``MiClase.f`` --- es un *objeto método*, no un objeto función.


.. _tut-methodobjects:

Objetos Método
--------------

Generalmente, un método es llamado luego de ser enlazado::

   x.f()

En el ejemplo :class:`MiClase`, esto devuelve la cadena ``'hola mundo'``.
Pero no es necesario llamar al método justo en ese momento: ``x.f`` es
un objeto método, y puede ser guardado y llamado más tarde.  Por ejemplo::

   xf = x.f
   while True:
       print xf()

continuará imprimiendo ``hola mundo`` hasta el fín de los días.

¿Que sucede exactamente cuando un método es llamado?  Debes haber notado que
``x.f()`` fue llamado más arriba sin ningún argumento, a pesar de que la definición
de función de :meth:`f` especificaba un argumento. ¿Que pasó con ese argumento?
Por supuesto que Python levanta una excepción cuando una función que requiere
un argumento es llamada sin ninguno --- aún si el argumento no es utilizado...

De hecho, tal vez hayas adivinado la respuesta: lo que tienen de especial los
métodos es que el objeto es pasado como el primer argumento de la función.
En nuestro ejemplo, la llamada ``x.f()`` es exáctamente equivalente a
``MiClase.f(x)``.  En general, llamar a un método con una lista de *n* argumentos
es equivalente a llamar a la función correspondiente con una lista de argumentos
que es creada insertando el objeto del método antes del primer argumento.

Si aún no comprendés como funcionan los métodos, un vistazo a la implementación
puede ayudar a clarificar este tema. Cuando un atributo de instancia es
referenciado y no es un atributo de datos, se busca dentro de su clase. Si
el nombre denota un atributo de clase válido que es un objeto función, un método 
objeto es creado, juntando (punteros a) el objeto instancia y el objeto función
que ha sido encontrado. Este objeto abstracto creado de esta unión es el objeto
método. Cuando el objeto método es llamado con una lista de argumentos, es
nuevamente desempacado, una lista de argumentos nueva es construida a partir del
objeto instancia y la lista de argumentos original, y el objeto función es llamado
con esta nueva lista de argumentos.


.. _tut-remarks:

Algunas observaciones
=====================

.. Tal vez se podrían colocar más cuidadosamente...

Los atributos de datos tienen preferencia sobre los métodos con el mismo
nombre; para evitar conflictos de nombre accidentales, que pueden causar
errores difíciles de encontrar en programas grandes, es prudente usar algún
tipo de convención que minimice las posibilidades de dichos conflictos.
Algunas convenciones pueden ser poner los nombres de métodos con mayúsculas,
prefijar los nombres de atributos de datos con una pequeña cadena única (a lo
mejor sólo un guión bajo), o usar verbos para los métodos y sustantivos para
los atributos.

A los atributos de datos los pueden referenciar tanto los métodos como los
usuarios ("clientes") ordinarios de un objeto.  En otras palabras, las clases
no se usan para implementar tipos de datos abstractos puros.  De hecho, en
Python no hay nada que haga que se cumpla el ocultamiento de datos --- todo se
basa en convención.  (Por otro lado, la implementación de Python, escrita en C,
puede ocultar por completo detalles de implementación y el control de acceso a
un objeto si es necesario; esto se puede usar en extensiones a Python escritas
en C.)

Los clientes deben usar los atributos de datos con cuidado --- éstos pueden
romper invariantes que mantenienen los métodos si pisan los atributos de datos.
Observá que los clientes pueden añadir sus propios atributos de datos a una
instancia sin afectar la validez de sus métodos, siempre y cuando se eviten
conflictos de nombres --- de nuevo, una convención de nombres puede ahorrar
un montón de dolores de cabeza.

No hay un atajo para referenciar atributos de datos (¡u otros métodos!) desde
dentro de un método.  A mi parecer, esto en realidad aumenta la legibilidad de
los métodos: no existe posibilidad alguna de confundir variables locales con
variables de instancia cuando repasamos un método.

A menudo, el primer argumento de un método se llama ``self`` (uno mismo).  Esto
no es nada más que una convención: el nombre ``self`` no significa nada en
especial para Python.  (Observá que, sin embargo, si no seguís la convención tu
código puede resultar menos legible a otros programadores de Python, y puede
llegar a pasar que un programa *navegador de clases* pueda escribirse de una
manera que dependa de dicha convención.)

Cualquier objeto función que es un atributo de clase define un método para
instancias de esa clase.  No es necesario que el la definición de la función
esté textualmente dentro de la definición de la clase: asignando un objeto
función a una variable local en la clase también está bien.  Por ejemplo::

   # Función definida fuera de la clase
   def f1(self, x, y):
       return min(x, x+y)

   class C:
       f = f1
       def g(self):
           return 'hola mundo'
       h = g

Ahora ``f``, ``g`` y ``h`` son todos atributos de la clase :class:`C` que hacen
referencia a objetos función, y consecuentemente son todos métodos de las
instancias de :class:`C` --- ``h`` siendo exactamente equivalente a ``g``.
Fijate que esta práctica normalmente sólo sirve para confundir al que lea un
programa.

Los métodos pueden llamar a otros métodos de la instancia usando el argumento
``self``::

   class Bolsa:
       def __init__(self):
           self.datos = []
       def agregar(self, x):
           self.datos.append(x)
       def dobleagregar(self, x):
           self.agregar(x)
           self.agregar(x)

Los métodos pueden referenciar nombres globales de la misma manera que lo hacen
las funciones comunes.  El alcance global asociado a un método es el módulo que
contiene la definición de la clase.  (¡La clase misma nunca se usa como un
alcance global!) Si bien es raro encontrar una buena razón para usar datos
globales en un método, hay muchos usos legítimos del alcance global: por lo
menos, las funciones y módulos importados en el alcance global pueden usarse
por los métodos, al igual que las funciones y clases definidas en él.
Habitualmente, la clase que contiene el método está definida en este alcance
global, y en la siguiente sección ¡veremos algunas buenas razones por las que
un método querría referenciar a su propia clase!

Todo valor es un objeto, y por lo tanto tiene una *clase* (también llamado su
*tipo*). Ésta se almacena como ``objeto.__class__``.


.. _tut-inheritance:

Herencia
========

Por supuesto, una característica del lenguaje no sería digna del nombre "clase"
si no soporta herencia.  La sintaxis para una definición de clase derivada se
ve así::

   class ClaseDerivada(ClaseBase):
       <declaración-1>
       .
       .
       .
       <declaración-N>

El nombre :class:`ClaseBase` debe estar definido en un alcance que contenga a
la definición de la clase derivada.  En el lugar del nombre de la clase base se
permiten otras expresiones arbitrarias.  Esto puede ser útil, por ejemplo,
cuando la clase base está definida en otro módulo::

   class ClaseDerivada(modulo.ClaseBase):

La ejecución de una definición de clase derivada procede de la misma forma que
una clase base.  Cuando el objeto clase se construye, se tiene en cuenta a la
clase base.  Esto se usa para resolver referencias a atributos: si un atributo
solicitado no se encuentra en la clase, la búsqueda continúa por la clase base.
Esta regla se aplica recursivamente si la clase base misma deriva de alguna
otra clase.

No hay nada en especial en la instanciación de clases derivadas:
``ClaseDerivada()`` crea una nueva instancia de la clase.  Las referencias a
métodos se resuelven de la siguiente manera: se busca el atributo de clase
correspondiente, descendiendo por la cadena de clases base si es necesario, y
la referencia al método es válida si se entrega un objeto función.

Las clases derivadas pueden redefinir métodos de su clase base.  Como los
métodos no tienen privilegios especiales cuando llaman a otros métodos del
mismo objeto, un método de la clase base que llame a otro método definido en la
misma clase base puede terminar llamando a un método de la clase derivada que
lo haya redefinido.  (Para los programadores de C++: en Python todos los
métodos son en efecto ``virtuales``.)

Un método redefinido en una clase derivada puede de hecho querer extender en
vez de simplemente reemplazar al método de la clase base con el mismo nombre.
Hay una manera simple de llamar al método de la clase base directamente:
simplemente llamás a ``ClaseBase.metodo(self, argumentos)``.  En ocasiones esto
es útil para los clientes también.  (Observá que esto sólo funciona si la clase
base está definida o importada directamente en el alcance global.)

Python tiene dos funciones integradas que funcionan con herencia:

* Usa :func:`isinstance` para verificar el tipo de un objeto:
  ``isinstance(obj, int)`` devuelve ``True`` solo si ``obj.__class__`` es
  :class:`int` o alguna clase derivada de :class:`int`.

* Usa :func:`issubclass` para comprobar herencia de clase:
  ``issubclass(bool, int)`` da ``True`` ya que :class:`bool` es una subclase de
  :class:`int`.  Sin embargo, ``issubclass(unicode, str)`` devuelve ``False``
  porque :class:`unicode` no es una subclase de :class:`str` (solamente tienen
  un ancestro en común, :class:`basestring`).



.. _tut-multiple:

Herencia múltiple
-----------------

Python soporta una forma limitada de herencia múltiple también.  Una definición
de clase con múltiples clases base se ve así::

   class ClaseDerivada(Base1, Base2, Base3):
       <declaración-1>
       .
       .
       .
       <declaración-N>

Para clases de estilo viejo la única regla es buscar en profundidad, de
izquierda a derecha.  Por lo tanto, si un atributo no se encuentra en
:class:`ClaseDerivada`, se busca en :class:`Base1`, luego (recursivamente) en
las clases base de :class:`Base1`, y sólo si no se encuentra allí se lo busca
en :class:`Base2`, y así sucesivamente.

(A algunos la búsqueda en anchura, o sea, buscar en :class:`Base2` y
:class:`Base3` antes que en las clases base de :class:`Base1`, les parece más
natural.  Sin embargo, para esto haría falta que sepás si un atributo en
particular de :class:`Base1` está de hecho definido en :class:`Base1` o en
alguna de sus clases base antes de que podás entender las consecuencias de un
conflicto de nombres con un atributo de :class:`Base2`.  La regla de buscar
primero en profundidad no hace diferencias entre atributos directos o heredados
de :class:`Base1`.)

Para las clases de :term:`estilo nuevo`, el método de resolución de orden
cambia dinámicamente para soportar llamadas cooperativas a :func:`super`.  Este
enfoque es conocido en otros lenguajes con herencia múltiple como "llámese al
siguiente método" y es más poderoso que la llamada al superior que se encuentra
en lenguajes con sólo herencia simple.

Con las clases de estilo nuevo, se necesita el orden dinámico porque todos los
casos de herencia múltiple exhiben una o más relaciones en diamante (cuando se
puede llegar a al menos una de las superclases por distintos caminos desde la
clase de más abajo).  Por ejemplo, todas las clases de nuevo estilo heredan de
:class:`object`, por lo tanto cualquier caso de herencia múltiple provee más de
un camino para llegar a :class:`object`.  Para que las clases base no sean
accedidas más de una vez, el algoritmo dinámico linealiza el orden de búsqueda
de manera que se preserve el orden de izquierda a derecha especificado en cada
clase, se llame a cada superclase sólo una vez, y que sea monótona (lo cual
significa que una clase puede tener subclases sin afectar el orden de
precedencia de sus superclases).  En conjunto, estas propiedades hacen posible
diseñar clases confiables y extensibles con herencia múltiple. Para más
detalles mirá  http://www.python.org/download/releases/2.3/mro/.


.. _tut-private:

Variables Privadas
==================

Hay soporte limitado para identificadores privados de clase.  Cualquier
identificador con la forma ``__spam`` (al menos dos guiones bajos al principio,
como mucho un guión bajo al final) es textualmente reemplazado por
``_nombredeclase__spam``, donde ``nombredeclase`` es el nombre de clase actual
al que se le sacan guiones bajos del comienzo (si los tuviera).  Se modifica el
nombre del indentificador sin importar su posición sintáctica, asi que puede ser
usado para definir instancias y variables de clase privadas, métodos, variables
guardadas en globales, y aún variables guardadas en instancias privadas de esta
clase en instancias de *otras* clases.  Puede ocurrir que se trunque si el
nombre modificado queda con más de 255 caractéres.  Fuera de las clases,
o cuando el nombre de clase consiste solo en guiones bajos, no se modifican los
nombres de identificadores.

La modificación de nombres se usa para darle a las clases una forma fácil de
definir variables de instancia y métodos "privados", sin tener que preocuparse
por variables de instancia definidas por clases derivadas, o que el código
fuera de la clase toquetee las variables de instancia.  Hay que aclarar que
las reglas de modificación de nombres están diseñadas principalmente para
evitar accidentes; es posible que un alma determinada acceda o modifique una
variable que es considerada como privada.  Esto hasta puede resultar útil en
circunstancias especiales, tales como en el depurador, y esa es una de las
razones por la que esta inconsistencia no se corrige. (Otra más: la derivación
de una clase usando el mismo nombre que la clase base hace que sea posible el
uso de variables privadas de la clase base.)

Notar que el código pasado a ``exec``, a ``eval()`` o a ``execfile()`` no
considera que el nombre de clase de la clase invocante sea la clase actual;
esto es similar al efecto de la sentencia ``global``, efecto que es de
similar manera restringido a código que es compilado a byte en conjunto. La
misma restricción aplica a ``getattr()``, ``setattr()`` y ``delattr()``, así
como cuando se referencia a ``__dict__`` directamente.


.. _tut-odds:

Cambalache
==========

A veces es útil tener un tipo de datos similar al "registro" de Pascal o la
"estructura" de C, que sirva para juntar algunos pocos items con nombre.  Una
definición de clase vacía funcionará perfecto::

   class Empleado:
       pass

   juan = Empleado() # Crear un registro de empleado vacío

   # Llenar los campos del registro
   juan.nombre = 'Juan Pistola'
   juan.depto = 'laboratorio de computación'
   juan.salario = 1000

Algún código Python que espera un tipo abstracto de datos en particular
puede frecuentemente recibir en cambio una clase que emula los métodos de aquel
tipo de datos.  Por ejemplo, si tenés una función que formatea algunos
datos a partir de un objeto archivo, podés definir una clase con métodos
:meth:`read` y :meth:`readline` que obtengan los datos de alguna cadena en
memoria intermedia, y pasarlo como argumento.

.. (Desafortunadamente esta técnica tiene sus limitaciones: una clase no
   puede definir operaciones que sean accedidas por sintaxis especiales tales
   como indexado de secuencias u operaciones aritméticas, y asignar un
   pseudo-archivo a sys.stdin no causará que el intérprete continúe leyendo
   desde ahí.)
   
Los objetos método de instancia tienen atributos también: ``m.im_self`` es
el objeto instancia con el método :meth:`m`, y ``m.im_func`` es el objeto
función correspondiente al método.


.. _tut-exceptionclasses:

Las excepciones son clases también
==================================

Las excepciones definidas por el usuario son identificadas por clases también.
Usando este mecanismo es posible crear jerarquías extensibles de excepciones::

Hay dos nuevas formas (semánticas) válidas para la sentencia raise::

   raise Clase, instancia

   raise instancia

En la primera forma, ``instancia`` debe ser una instancia de :class:`Clase` o
de una clase derivada de ella.  La segunda forma es una abreviatura de::

   raise instancia.__class__, instance

Una clase en una cláusula except es compatible con una excepción si es de la misma
clase o una clase base de la misma (pero no al revés --- una cláusula except
listando una clase derivada no es compatible con una clase base).  Por ejemplo,
el siguiente código imprimirá B, C, D en ese orden::

   class B:
       pass
   class C(B):
       pass
   class D(C):
       pass

   for c in [B, C, D]:
       try:
           raise c()
       except D:
           print "D"
       except C:
           print "C"
       except B:
           print "B"

Notar que si la cláusulas except fueran invertidas (dejando ``except B`` al
principio), habría impreso B, B, B --- la primera cláusula except que coincide
es disparada.

Cuando un mensaje de error se imprime para una excepción sin atrapar, se imprime
el nombre de la clase de la excepción, luego dos puntos y un espacio y
finalmente la instancia convertida a un string usando la función built-in :func:`str`.


.. _tut-iterators:

Iteradores
==========

Es probable que hayas notado que la mayoría de los objetos contenedores pueden
ser recorridos usando una sentencia :keyword:`for`::

   for elemento in [1, 2, 3]:
       print elemento
   for elemento in (1, 2, 3):
       print elemento
   for clave in {'uno':1, 'dos':2}:
       print clave
   for caracter in "123":
       print caracter
   for linea in open("miarchivo.txt"):
       print linea

Este estilo de acceso es limpio, conciso y conveniente.  El uso de iteradores
está impregnado y unifica a Python.  Detrás de bambalinas, la sentencia :keyword:`for`
llama a :func:`iter` en el objeto contenedor.  La función devuelve un objeto
iterador que define el método :meth:`next` que accede elementos en el contenedor
de a uno por vez.  Cuando no hay más elementos, :meth:`next` levanta una
excepción :exc:`StopIteration` que le avisa al bucle del :keyword:`for` que
hay que terminar. Este ejemplo muestra como funciona todo esto::

   >>> s = 'abc'
   >>> it = iter(s)
   >>> it
   <iterator object at 0x00A1DB50>
   >>> it.next()
   'a'
   >>> it.next()
   'b'
   >>> it.next()
   'c'
   >>> it.next()

   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
       it.next()
   StopIteration

Habiendo visto la mecánica del protocolo de iteración, es fácil agregar
comportamiento de iterador a tus clases.  Definí un método :meth:`__iter__`
que devuelva un objeto con un método :meth:`next`.  Si la clase define
:meth:`next`, entonces alcanza con que :meth:`__iter__` devuelva ``self``::

   class Reversa:
       "Iterador para recorrer una secuencia marcha atrás"
       def __init__(self, datos):
           self.datos = datos
           self.indice = len(datos)
       def __iter__(self):
           return self
       def next(self):
           if self.indice == 0:
               raise StopIteration
           self.indice = self.indice - 1
           return self.datos[self.indice]

   >>> for letra in Reversa('spam'):
   ...     print letra
   ...
   m
   a
   p
   s


.. _tut-generators:

Generadores
===========

Los :term:`Generador`\es son una simple y poderosa herramienta para crear
iteradores.  Se escriben como funciones regulares pero usan la sentencia
:keyword:`yield` cuando quieren devolver datos.  Cada vez que :meth:`next` 
es llamado, el generador continúa desde donde dejó (y recuerda todos los
valores de datos y cual sentencia fue ejecutada última).  Un ejemplo muestra
que los generadores pueden ser muy fáciles de crear::

   def reversa(datos):
       for indice in range(len(datos)-1, -1, -1):
           yield datos[indice]

   >>> for letra in reversa('golf'):
   ...     print letra
   ...
   f
   l
   o
   g	

Todo lo que puede ser hecho con generadores también puede ser hecho con
iteradores basados en clases, como se describe en la sección anterior.  Lo
que hace que los generadores sean tan compactos es que los métodos
:meth:`__iter__` y :meth:`next` son creados automáticamente.

Otra característica clave es que las variables locales y el estado de la
ejecución son guardados automáticamente entre llamadas.  Esto hace que la
función sea más fácil de escribir y quede mucho más claro que hacerlo
usando variables de instancia tales como ``self.indice`` y ``self.datos``.

Además de la creación automática de métodos y el guardar el estado del
programa, cuando los generadores terminan levantan automáticamente 
:exc:`StopIteration`.  Combinadas, estas características facilitan
la creación de iteradores, y hacen que no sea más esfuerzo que escribir
una función regular.


.. _tut-genexps:

Expresiones Generadoras
=======================

Algunos generadores simples pueden ser codificados concisamente como
expresiones usando una sintaxis similar a las listas por comprensión pero con
paréntesis en vez de corchetes.  Estas expresiones se utilizan en
situaciones donde el generador es usado inmediatamente por una función que
lo contiene.  Las expresiones generadoras son más compactas pero menos
versátiles que definiciones completas de generadores, y tienden a utilizar
menos memoria que las listas por comprensión equivalentes.

Ejemplos::

   >>> sum(i*i for i in range(10))                 # suma de cuadrados
   285

   >>> xvec = [10, 20, 30]
   >>> yvec = [7, 5, 3]
   >>> sum(x*y for x,y in zip(xvec, yvec))         # producto escalar
   260

   >>> from math import pi, sin
   >>> tabla_de_senos = dict((x, sin(x*pi/180)) for x in range(0, 91))

   >>> palabras_unicas = set(word  for line in page  for word in line.split())

   >>> mejor_promedio = max((estudiante.promedio, estudiante.nombre) for estudiante in graduados)

   >>> data = 'golf'
   >>> list(data[i] for i in range(len(data)-1,-1,-1))
   ['f', 'l', 'o', 'g']



.. rubric:: Footnotes

.. [#] Excepto una cosita. Los objetos módulo tienen un atributo secreto de solo
   lectura llamado :attr:`__dict__` que devuelve el diccionario usado para
   implementar el espacio de nombres del módulo; el nombre :attr:`__dict__` es un
   atributo, pero no es un nombre global. Obviamente, esto viola la abstracción de
   la implementación de espacios de nombres, y debe ser restringido a cosas tales
   como depuradores post-mortem.
