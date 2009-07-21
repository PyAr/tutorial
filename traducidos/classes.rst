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

Method Objects
--------------

Usually, a method is called right after it is bound::

   x.f()

In the :class:`MyClass` example, this will return the string ``'hello world'``.
However, it is not necessary to call a method right away: ``x.f`` is a method
object, and can be stored away and called at a later time.  For example::

   xf = x.f
   while True:
       print xf()

will continue to print ``hello world`` until the end of time.

What exactly happens when a method is called?  You may have noticed that
``x.f()`` was called without an argument above, even though the function
definition for :meth:`f` specified an argument.  What happened to the argument?
Surely Python raises an exception when a function that requires an argument is
called without any --- even if the argument isn't actually used...

Actually, you may have guessed the answer: the special thing about methods is
that the object is passed as the first argument of the function.  In our
example, the call ``x.f()`` is exactly equivalent to ``MyClass.f(x)``.  In
general, calling a method with a list of *n* arguments is equivalent to calling
the corresponding function with an argument list that is created by inserting
the method's object before the first argument.

If you still don't understand how methods work, a look at the implementation can
perhaps clarify matters.  When an instance attribute is referenced that isn't a
data attribute, its class is searched.  If the name denotes a valid class
attribute that is a function object, a method object is created by packing
(pointers to) the instance object and the function object just found together in
an abstract object: this is the method object.  When the method object is called
with an argument list, it is unpacked again, a new argument list is constructed
from the instance object and the original argument list, and the function object
is called with this new argument list.


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

Odds and Ends
=============

Sometimes it is useful to have a data type similar to the Pascal "record" or C
"struct", bundling together a few named data items.  An empty class definition
will do nicely::

   class Employee:
       pass

   john = Employee() # Create an empty employee record

   # Fill the fields of the record
   john.name = 'John Doe'
   john.dept = 'computer lab'
   john.salary = 1000

A piece of Python code that expects a particular abstract data type can often be
passed a class that emulates the methods of that data type instead.  For
instance, if you have a function that formats some data from a file object, you
can define a class with methods :meth:`read` and :meth:`readline` that get the
data from a string buffer instead, and pass it as an argument.

.. (Unfortunately, this technique has its limitations: a class can't define
   operations that are accessed by special syntax such as sequence subscripting
   or arithmetic operators, and assigning such a "pseudo-file" to sys.stdin will
   not cause the interpreter to read further input from it.)

Instance method objects have attributes, too: ``m.im_self`` is the instance
object with the method :meth:`m`, and ``m.im_func`` is the function object
corresponding to the method.


.. _tut-exceptionclasses:

Exceptions Are Classes Too
==========================

User-defined exceptions are identified by classes as well.  Using this mechanism
it is possible to create extensible hierarchies of exceptions.

There are two new valid (semantic) forms for the raise statement::

   raise Class, instance

   raise instance

In the first form, ``instance`` must be an instance of :class:`Class` or of a
class derived from it.  The second form is a shorthand for::

   raise instance.__class__, instance

A class in an except clause is compatible with an exception if it is the same
class or a base class thereof (but not the other way around --- an except clause
listing a derived class is not compatible with a base class).  For example, the
following code will print B, C, D in that order::

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

Note that if the except clauses were reversed (with ``except B`` first), it
would have printed B, B, B --- the first matching except clause is triggered.

When an error message is printed for an unhandled exception, the exception's
class name is printed, then a colon and a space, and finally the instance
converted to a string using the built-in function :func:`str`.


.. _tut-iterators:

Iterators
=========

By now you have probably noticed that most container objects can be looped over
using a :keyword:`for` statement::

   for element in [1, 2, 3]:
       print element
   for element in (1, 2, 3):
       print element
   for key in {'one':1, 'two':2}:
       print key
   for char in "123":
       print char
   for line in open("myfile.txt"):
       print line

This style of access is clear, concise, and convenient.  The use of iterators
pervades and unifies Python.  Behind the scenes, the :keyword:`for` statement
calls :func:`iter` on the container object.  The function returns an iterator
object that defines the method :meth:`next` which accesses elements in the
container one at a time.  When there are no more elements, :meth:`next` raises a
:exc:`StopIteration` exception which tells the :keyword:`for` loop to terminate.
This example shows how it all works::

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

Having seen the mechanics behind the iterator protocol, it is easy to add
iterator behavior to your classes.  Define a :meth:`__iter__` method which
returns an object with a :meth:`next` method.  If the class defines
:meth:`next`, then :meth:`__iter__` can just return ``self``::

   class Reverse:
       "Iterator for looping over a sequence backwards"
       def __init__(self, data):
           self.data = data
           self.index = len(data)
       def __iter__(self):
           return self
       def next(self):
           if self.index == 0:
               raise StopIteration
           self.index = self.index - 1
           return self.data[self.index]

   >>> for char in Reverse('spam'):
   ...     print char
   ...
   m
   a
   p
   s


.. _tut-generators:

Generators
==========

:term:`Generator`\s are a simple and powerful tool for creating iterators.  They
are written like regular functions but use the :keyword:`yield` statement
whenever they want to return data.  Each time :meth:`next` is called, the
generator resumes where it left-off (it remembers all the data values and which
statement was last executed).  An example shows that generators can be trivially
easy to create::

   def reverse(data):
       for index in range(len(data)-1, -1, -1):
           yield data[index]

   >>> for char in reverse('golf'):
   ...     print char
   ...
   f
   l
   o
   g	

Anything that can be done with generators can also be done with class based
iterators as described in the previous section.  What makes generators so
compact is that the :meth:`__iter__` and :meth:`next` methods are created
automatically.

Another key feature is that the local variables and execution state are
automatically saved between calls.  This made the function easier to write and
much more clear than an approach using instance variables like ``self.index``
and ``self.data``.

In addition to automatic method creation and saving program state, when
generators terminate, they automatically raise :exc:`StopIteration`. In
combination, these features make it easy to create iterators with no more effort
than writing a regular function.


.. _tut-genexps:

Generator Expressions
=====================

Some simple generators can be coded succinctly as expressions using a syntax
similar to list comprehensions but with parentheses instead of brackets.  These
expressions are designed for situations where the generator is used right away
by an enclosing function.  Generator expressions are more compact but less
versatile than full generator definitions and tend to be more memory friendly
than equivalent list comprehensions.

Examples::

   >>> sum(i*i for i in range(10))                 # sum of squares
   285

   >>> xvec = [10, 20, 30]
   >>> yvec = [7, 5, 3]
   >>> sum(x*y for x,y in zip(xvec, yvec))         # dot product
   260

   >>> from math import pi, sin
   >>> sine_table = dict((x, sin(x*pi/180)) for x in range(0, 91))

   >>> unique_words = set(word  for line in page  for word in line.split())

   >>> valedictorian = max((student.gpa, student.name) for student in graduates)

   >>> data = 'golf'
   >>> list(data[i] for i in range(len(data)-1,-1,-1))
   ['f', 'l', 'o', 'g']



.. rubric:: Footnotes

.. [#] Except for one thing.  Module objects have a secret read-only attribute called
   :attr:`__dict__` which returns the dictionary used to implement the module's
   namespace; the name :attr:`__dict__` is an attribute but not a global name.
   Obviously, using this violates the abstraction of namespace implementation, and
   should be restricted to things like post-mortem debuggers.

