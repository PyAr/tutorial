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

Un Primer Vistazo a las Clases
==============================

Las clases agregan un poco de sintaxis nueva, tres nuevos tipos de objetos y
algo de semántica nueva.


.. _tut-classdefinition:

Syntaxis de Definición de Clases
--------------------------------

La forma más sencilla de definición de clase se ve así::

   class NombreDeClase:
       <sentencia-1>
       .
       .
       .
       <sentencia-N>

Las definiciones de clases, tal como las definiciones de funciones (sentencias
:keyword:`def`) deben ser ejecutadas antes de que tengan algún efecto.  (Si
quisieras podrías colocar una definición de clase en un bloque de una sentencia
:keyword:`if`, o dentro de una función.)

En la práctica, las sentencias dentro de una definición de clase generalmente
serán definiciones de funciones, pero se permiten otras sentencias y a veces
son útiles --- veremos esto más adelante.  Las definiciones de funciones dentro
de una clase normalmente tienen una forma peculiar de lista de argumentos, que
está dada por las convenciones de llamadas para los métodos --- esto también
será explicado luego. 

Cuando se ingresa a una definición de clase, se crea un nuevo espacio de nombres,
y es usado como el ámbito local --- por lo tanto, todas las asignaciones a variables
locales quedan dentro de este nuevo espacio de nombres.  En particular, las
definiciones de funciones enlazan el nombre de la nueva función aquí.

Cuando se sale normalmente de la definición de una clase (por el final), se crea un
*objeto clase*.  Esto es básicamente un envoltorio de los contenidos del espacio de
nombres creado por la definición de clase; veremos más sobre los objetos clase en
la próxima sección.  El ámbito local original (el que estaba en efecto justo antes
de ingresar a la definición de clase) se restaura, y el objeto clase se enlaza aquí
al nombre de la clase dado en el encabezado de la definición de clase
(:class:`NombreDeClase` en el ejemplo).


.. _tut-classobjects:

Objetos Clase
-------------

Los objetos clase soportan dos tipos de operaciones: referenciar atributos e
instanciación.

Para *referenciar atributos* se usa la sintaxis estandard que es usada para todas las
referencias a atributos en Python: ``objeto.nombre``.  Nombres válidos de atributos
son todos los nombres que estaban en el espacio de nombre de la clase en el momento
que el objeto clase fue creado.  Por lo tanto, si la definición de clase fuera así::

   class MiClase:
       "Una clase de ejemplo simple"
       i = 12345
       def f(self):
           return 'hola mundo'

entonces ``MiClase.i`` y ``MiClase.f`` son referencias de atributos válidas, que
devuelven un entero y un objeto función, respectivamente. También se le puede
asignar a los atributos de clase, asi que podés cambiar el valor de ``MiClase.i``
mediante la asignación.  :attr:`__doc__` es también un atributo válido, que
devuelve el docstring que pertenece a la clase: ``"Una clase de ejemplo simple"``.

La *instanciación* de clase usa notación de función.  Tan solo hacé de cuenta
que el objeto clase es una función que no recibe parámetros, y que devuelve una 
nueva instancia de la clase.
Por ejemplo (asumiendo la clase anterior)::

   x = MiClase()

crea un nueva *instancia* de la clase y asigna este objeto a la variable
local ``x``.

La operación de instanciación ("llamar" a un objeto clase) crea un objeto vacío.
Muchas clases desean crear objetos con instancias personalizadas con un estado
inicial específico.  Por lo tanto la clase puede definir un método especial
llamado :meth:`__init__`, de esta forma::

   def __init__(self):
       self.datos = []

Cuando una clase define un método :meth:`__init__`, la instanciación de clase
automáticamente invoca a :meth:`__init__` para la instancia de clase recién creada.
Entonces en este ejemplo, una instancia nueva e inicializada puede ser obtenida así::

   x = MiClase()

Por supuesto, el método :meth:`__init__` puede tener argumentos para mayor
flexibilidad. En tal caso, los argumentos dados al operador de instanciación de clase
son pasados a su vez a :meth:`__init__`.  Por ejemplo, ::

   >>> class Complejo:
   ...     def __init__(self, partereal, parteimag):
   ...         self.r = partereal
   ...         self.i = parteimag
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

Random Remarks
==============

.. These should perhaps be placed more carefully...

Data attributes override method attributes with the same name; to avoid
accidental name conflicts, which may cause hard-to-find bugs in large programs,
it is wise to use some kind of convention that minimizes the chance of
conflicts.  Possible conventions include capitalizing method names, prefixing
data attribute names with a small unique string (perhaps just an underscore), or
using verbs for methods and nouns for data attributes.

Data attributes may be referenced by methods as well as by ordinary users
("clients") of an object.  In other words, classes are not usable to implement
pure abstract data types.  In fact, nothing in Python makes it possible to
enforce data hiding --- it is all based upon convention.  (On the other hand,
the Python implementation, written in C, can completely hide implementation
details and control access to an object if necessary; this can be used by
extensions to Python written in C.)

Clients should use data attributes with care --- clients may mess up invariants
maintained by the methods by stamping on their data attributes.  Note that
clients may add data attributes of their own to an instance object without
affecting the validity of the methods, as long as name conflicts are avoided ---
again, a naming convention can save a lot of headaches here.

There is no shorthand for referencing data attributes (or other methods!) from
within methods.  I find that this actually increases the readability of methods:
there is no chance of confusing local variables and instance variables when
glancing through a method.

Often, the first argument of a method is called ``self``.  This is nothing more
than a convention: the name ``self`` has absolutely no special meaning to
Python.  (Note, however, that by not following the convention your code may be
less readable to other Python programmers, and it is also conceivable that a
*class browser* program might be written that relies upon such a convention.)

Any function object that is a class attribute defines a method for instances of
that class.  It is not necessary that the function definition is textually
enclosed in the class definition: assigning a function object to a local
variable in the class is also ok.  For example::

   # Function defined outside the class
   def f1(self, x, y):
       return min(x, x+y)

   class C:
       f = f1
       def g(self):
           return 'hello world'
       h = g

Now ``f``, ``g`` and ``h`` are all attributes of class :class:`C` that refer to
function objects, and consequently they are all methods of instances of
:class:`C` --- ``h`` being exactly equivalent to ``g``.  Note that this practice
usually only serves to confuse the reader of a program.

Methods may call other methods by using method attributes of the ``self``
argument::

   class Bag:
       def __init__(self):
           self.data = []
       def add(self, x):
           self.data.append(x)
       def addtwice(self, x):
           self.add(x)
           self.add(x)

Methods may reference global names in the same way as ordinary functions.  The
global scope associated with a method is the module containing the class
definition.  (The class itself is never used as a global scope!)  While one
rarely encounters a good reason for using global data in a method, there are
many legitimate uses of the global scope: for one thing, functions and modules
imported into the global scope can be used by methods, as well as functions and
classes defined in it.  Usually, the class containing the method is itself
defined in this global scope, and in the next section we'll find some good
reasons why a method would want to reference its own class!

Each value is an object, and therefore has a *class* (also called its *type*).
It is stored as ``object.__class__``.


.. _tut-inheritance:

Inheritance
===========

Of course, a language feature would not be worthy of the name "class" without
supporting inheritance.  The syntax for a derived class definition looks like
this::

   class DerivedClassName(BaseClassName):
       <statement-1>
       .
       .
       .
       <statement-N>

The name :class:`BaseClassName` must be defined in a scope containing the
derived class definition.  In place of a base class name, other arbitrary
expressions are also allowed.  This can be useful, for example, when the base
class is defined in another module::

   class DerivedClassName(modname.BaseClassName):

Execution of a derived class definition proceeds the same as for a base class.
When the class object is constructed, the base class is remembered.  This is
used for resolving attribute references: if a requested attribute is not found
in the class, the search proceeds to look in the base class.  This rule is
applied recursively if the base class itself is derived from some other class.

There's nothing special about instantiation of derived classes:
``DerivedClassName()`` creates a new instance of the class.  Method references
are resolved as follows: the corresponding class attribute is searched,
descending down the chain of base classes if necessary, and the method reference
is valid if this yields a function object.

Derived classes may override methods of their base classes.  Because methods
have no special privileges when calling other methods of the same object, a
method of a base class that calls another method defined in the same base class
may end up calling a method of a derived class that overrides it.  (For C++
programmers: all methods in Python are effectively ``virtual``.)

An overriding method in a derived class may in fact want to extend rather than
simply replace the base class method of the same name. There is a simple way to
call the base class method directly: just call ``BaseClassName.methodname(self,
arguments)``.  This is occasionally useful to clients as well.  (Note that this
only works if the base class is defined or imported directly in the global
scope.)

Python has two builtin functions that work with inheritance:

* Use :func:`isinstance` to check an object's type: ``isinstance(obj, int)``
  will be ``True`` only if ``obj.__class__`` is :class:`int` or some class
  derived from :class:`int`.

* Use :func:`issubclass` to check class inheritance: ``issubclass(bool, int)``
  is ``True`` since :class:`bool` is a subclass of :class:`int`.  However,
  ``issubclass(unicode, str)`` is ``False`` since :class:`unicode` is not a
  subclass of :class:`str` (they only share a common ancestor,
  :class:`basestring`).



.. _tut-multiple:

Multiple Inheritance
--------------------

Python supports a limited form of multiple inheritance as well.  A class
definition with multiple base classes looks like this::

   class DerivedClassName(Base1, Base2, Base3):
       <statement-1>
       .
       .
       .
       <statement-N>

For old-style classes, the only rule is depth-first, left-to-right.  Thus, if an
attribute is not found in :class:`DerivedClassName`, it is searched in
:class:`Base1`, then (recursively) in the base classes of :class:`Base1`, and
only if it is not found there, it is searched in :class:`Base2`, and so on.

(To some people breadth first --- searching :class:`Base2` and :class:`Base3`
before the base classes of :class:`Base1` --- looks more natural.  However, this
would require you to know whether a particular attribute of :class:`Base1` is
actually defined in :class:`Base1` or in one of its base classes before you can
figure out the consequences of a name conflict with an attribute of
:class:`Base2`.  The depth-first rule makes no differences between direct and
inherited attributes of :class:`Base1`.)

For :term:`new-style class`\es, the method resolution order changes dynamically
to support cooperative calls to :func:`super`.  This approach is known in some
other multiple-inheritance languages as call-next-method and is more powerful
than the super call found in single-inheritance languages.

With new-style classes, dynamic ordering is necessary because all  cases of
multiple inheritance exhibit one or more diamond relationships (where one at
least one of the parent classes can be accessed through multiple paths from the
bottommost class).  For example, all new-style classes inherit from
:class:`object`, so any case of multiple inheritance provides more than one path
to reach :class:`object`.  To keep the base classes from being accessed more
than once, the dynamic algorithm linearizes the search order in a way that
preserves the left-to-right ordering specified in each class, that calls each
parent only once, and that is monotonic (meaning that a class can be subclassed
without affecting the precedence order of its parents).  Taken together, these
properties make it possible to design reliable and extensible classes with
multiple inheritance.  For more detail, see
http://www.python.org/download/releases/2.3/mro/.


.. _tut-private:

Private Variables
=================

There is limited support for class-private identifiers.  Any identifier of the
form ``__spam`` (at least two leading underscores, at most one trailing
underscore) is textually replaced with ``_classname__spam``, where ``classname``
is the current class name with leading underscore(s) stripped.  This mangling is
done without regard to the syntactic position of the identifier, so it can be
used to define class-private instance and class variables, methods, variables
stored in globals, and even variables stored in instances. private to this class
on instances of *other* classes.  Truncation may occur when the mangled name
would be longer than 255 characters. Outside classes, or when the class name
consists of only underscores, no mangling occurs.

Name mangling is intended to give classes an easy way to define "private"
instance variables and methods, without having to worry about instance variables
defined by derived classes, or mucking with instance variables by code outside
the class.  Note that the mangling rules are designed mostly to avoid accidents;
it still is possible for a determined soul to access or modify a variable that
is considered private.  This can even be useful in special circumstances, such
as in the debugger, and that's one reason why this loophole is not closed.
(Buglet: derivation of a class with the same name as the base class makes use of
private variables of the base class possible.)

Notice that code passed to ``exec``, ``eval()`` or ``execfile()`` does not
consider the classname of the invoking  class to be the current class; this is
similar to the effect of the  ``global`` statement, the effect of which is
likewise restricted to  code that is byte-compiled together.  The same
restriction applies to ``getattr()``, ``setattr()`` and ``delattr()``, as well
as when referencing ``__dict__`` directly.


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
