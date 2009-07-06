.. _tut-errors:

*********************
Errores y excepciones
*********************

Hasta ahora los mensajes de error no habían sido más que mencionados, pero si
intentaste los ejemplos probablemente hayas visto algunos.  Hay (al menos) dos
tipos diferentes de errores: *errores de sintaxis* y *excepciones*.


.. _tut-syntaxerrors:

Errores de sintaxis
===================

Los errores de sintaxis, también conocidos como errores de interpretación, son
quizás el tipo de queja más común que tenés cuando todavía estás aprendiendo
Python::

   >>> while True print 'Hola mundo'
     File "<stdin>", line 1, in ?
       while True print 'Hola mundo'
                      ^
   SyntaxError: invalid syntax

El intérprete repite la linea culpable y muestra una pequeña 'flecha'
que apunta al primer lugar donde se detectó el error.  Este es causado por (o
al menos detectado en) el símbolo que *precede* a la flecha: en el ejemplo,
el error se detecta en el :keyword:`print`, ya que faltan dos puntos (``':'``)
antes del mismo.  Se muestran el nombre del archivo y el número de linea para
que sepas dónde mirar en caso de que la entrada venga de un programa.


.. _tut-exceptions:

Excepciones
===========

Incluso si la declaración o expresión es sintácticamente correcta, puede
generar un error cuando se intenta ejecutarla.  Los errores detectados durante
la ejecución se llaman *excepciones*, y no son incondicionalmente fatales:
pronto aprenderás cómo manejarlos en los programas en Python.  Sin embargo, la
mayoría de las excepciones no son manejadas por los programas, y resultan en
mensajes de error como los mostrados aquí::

   >>> 10 * (1/0)
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ZeroDivisionError: integer division or modulo by zero
   >>> 4 + spam*3
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   NameError: name 'spam' is not defined
   >>> '2' + 2
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: cannot concatenate 'str' and 'int' objects

La última linea de los mensajes de error indica qué sucedió.  Las excepciones
vienen de distintos tipos, y el tipo se imprime como parte del mensaje: los
tipos en el ejemplo son: :exc:`ZeroDivisionError`, :exc:`NameError` y
:exc:`TypeError`.  La cadena mostrada como tipo de la excepción es el nombre de
la excepción integrada que ocurrió.  Esto es verdad para todas las excepciones
integradas al intérprete, pero no necesita ser verdad para excepciones
definidas por el usuario (aunque es una convención útil).  Los nombres de las
excepciones estándar son identificadores integrados al intérprete (no son
palabras clave reservadas).

El resto de la linea provee un detalle basado en el tipo de la excepción y qué
la causó.

La parte anterior del mensaje de error muestra el contexto donde la excepción
sucedió, en la forma de un *stack traceback* listando lineas fuente; sin
embargo, no mostrará lineas leídas de la entrada estándar.  El *traceback*
es el listado del *stack* de funciones por los cuales pasó la excepción
generada, indicando las mismas y más datos para analizar mejor el problema.

:ref:`bltin-exceptions` lista las excepciones integradas y sus significados.


.. _tut-handling:

Manejando excepciones
=====================

Es posible escribir programas que manejen las excepciones que quiera.  Mirá el
siguiente ejemplo, que le pide al usuario una entrada hasta que ingrese un
entero válido, pero permite al usuario interrumpir el programa (usando
:kbd:`Control-C` o lo que sea que el sistema operativo soporte); notá que una
interrupción generada por el usuario se señaliza generando la excepción
:exc:`KeyboardInterrupt`. ::

   >>> while True:
   ...     try:
   ...         x = int(raw_input(u"Por favor ingrese un número: "))
   ...         break
   ...     except ValueError:
   ...         print u"Oops!  No era válido.  Intente nuevamente..."
   ...

La declaración :keyword:`try` funciona de la siguiente manera:

* Primero, se ejecuta el *bloque try* (el código entre las declaraciones
  :keyword:`try` y :keyword:`except`).

* Si no ocurre ninguna excepción, el *bloque except* se saltea y termina la
  ejecución de la declaración :keyword:`try`.

* Si ocurre una excepción durante la ejecución del *bloque try*, el resto del
  bloque se saltea.  Luego, si su tipo coincide con la excepción nombrada luego
  del :keyword:`except`, se ejecuta el *bloque except*, y la ejecución continúa
  luego de la declaración :keyword:`try`.

* Si ocurre una excepción que no coincide con la excepción nombrada en el
  :keyword:`except`, esta se pasa a declaraciones :keyword:`try` de más afuera;
  si no se encuentra a nada que la maneje, es una *excepción no manejada*, y la
  ejecución se frena con un mensaje como los mostrado arriba.

Una declaración :keyword:`try` puede tener más de un :keyword:`except`, para
especificar manejadores para distintas excepciones. A lo sumo un manejador será
ejecutado.  Sólo se manejan excepciones que ocurren en el correspondiente
:keyword:`try`, no en otros manejadores del mismo :keyword:`try`.  Un
:keyword:`except` puede nombrar múltiples excepciones usando paréntesis, por
ejemplo::

   ... except (RuntimeError, TypeError, NameError):
   ...     pass

El último :keyword:`except` puede omitir nombrar qué excepción captura, para
servir como comodín.  Usá esto con extremo cuidado, ya que de esta manera es
fácil ocultar un error real de programación.  También puede usarse para mostrar
un mensaje de error y luego re-generar la excepción (permitiéndole al que llama
manejar también la excepción)::

   import sys

   try:
       f = open('miarchivo.txt')
       s = f.readline()
       i = int(s.strip())
   except IOError as (errno, strerror):
       print "Error E/S ({0}): {1}".format(errno, strerror)
   except ValueError:
       print "No pude convertir el dato a un entero."
   except:
       print "Error inesperado:", sys.exc_info()[0]
       raise

Las declaraciones :keyword:`try` ... :keyword:`except` tienen un *bloque else*
opcional, el cual, cuando está presente, debe seguir a los except.  Es útil
para aquel código que debe ejecutarse si el *bloque try* no genera una
excepción.  Por ejemplo::

   for arg in sys.argv[1:]:
       try:
           f = open(arg, 'r')
       except IOError:
           print 'no pude abrir', arg
       else:
           print arg, 'tiene', len(f.readlines()), 'lineas'
           f.close()

El uso del :keyword:`else` es mejor que agregar código adicional en el
:keyword:`try` poruqe evita capturar accidentalmente una excepción que no fue
generada por el código que está protegido por la declaración :keyword:`try` ...
:keyword:`except`.

Cuando ocurre una excepción, puede tener un valor asociado, también conocido
como el *argumento* de la excepción.  La presencia y el tipo de argumento
depende del tipo de excepción.

El :keyword:`except` puede especificar una variable luego del nombre (o tupla)
de excepción(es).  La variable se vincula a una instancia de excepción con los
argumentos almacenados en ``instance.args``.  Por conveniencia, la instancia
de excepción define :meth:`__getitem__` y :meth:`__str__` para que se pueda
acceder o mostrar los argumentos directamente, sin necesidad de hacer
referencia a ``.args``.

Pero se recomienda no usar ``.args``.  En cambio, el uso preferido es pasar un
único argumento a la excepción (que puede ser una tupla se se necesitan varios
argumentos) y vincularlo al atributo ``message``.  Uno también puede instanciar
una excepción antes de generarla, y agregarle cualquier atributo que uno desee::

   >>> try:
   ...    raise Exception('carne', 'huevos')
   ... except Exception as inst:
   ...    print type(inst)     # la instancia de excepción
   ...    print inst.args      # argumentos guardados en .args
   ...    print inst           # __str__ permite imprimir args directamente
   ...    x, y = inst          # __getitem__ permite usar args directamente
   ...    print 'x =', x
   ...    print 'y =', y
   ...
   <type 'exceptions.Exception'>
   ('carne', 'huevos')
   ('carne', 'huevos')
   x = carne
   y = huevos

Si una excepción tiene un argumento, este se imprime como la última parte (el
'detalle') del mensaje para las excepciones que no están manejadas.

Exception handlers don't just handle exceptions if they occur immediately in the
try clause, but also if they occur inside functions that are called (even
indirectly) in the try clause. For example::

   >>> def this_fails():
   ...     x = 1/0
   ...
   >>> try:
   ...     this_fails()
   ... except ZeroDivisionError as detail:
   ...     print 'Handling run-time error:', detail
   ...
   Handling run-time error: integer division or modulo by zero


.. _tut-raising:

Raising Exceptions
==================

The :keyword:`raise` statement allows the programmer to force a specified
exception to occur. For example::

   >>> raise NameError, 'HiThere'
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   NameError: HiThere

The first argument to :keyword:`raise` names the exception to be raised.  The
optional second argument specifies the exception's argument.  Alternatively, the
above could be written as ``raise NameError('HiThere')``.  Either form works
fine, but there seems to be a growing stylistic preference for the latter.

If you need to determine whether an exception was raised but don't intend to
handle it, a simpler form of the :keyword:`raise` statement allows you to
re-raise the exception::

   >>> try:
   ...     raise NameError, 'HiThere'
   ... except NameError:
   ...     print 'An exception flew by!'
   ...     raise
   ...
   An exception flew by!
   Traceback (most recent call last):
     File "<stdin>", line 2, in ?
   NameError: HiThere


.. _tut-userexceptions:

User-defined Exceptions
=======================

Programs may name their own exceptions by creating a new exception class.
Exceptions should typically be derived from the :exc:`Exception` class, either
directly or indirectly.  For example::

   >>> class MyError(Exception):
   ...     def __init__(self, value):
   ...         self.value = value
   ...     def __str__(self):
   ...         return repr(self.value)
   ...
   >>> try:
   ...     raise MyError(2*2)
   ... except MyError as e:
   ...     print 'My exception occurred, value:', e.value
   ...
   My exception occurred, value: 4
   >>> raise MyError, 'oops!'
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   __main__.MyError: 'oops!'

In this example, the default :meth:`__init__` of :class:`Exception` has been
overridden.  The new behavior simply creates the *value* attribute.  This
replaces the default behavior of creating the *args* attribute.

Exception classes can be defined which do anything any other class can do, but
are usually kept simple, often only offering a number of attributes that allow
information about the error to be extracted by handlers for the exception.  When
creating a module that can raise several distinct errors, a common practice is
to create a base class for exceptions defined by that module, and subclass that
to create specific exception classes for different error conditions::

   class Error(Exception):
       """Base class for exceptions in this module."""
       pass

   class InputError(Error):
       """Exception raised for errors in the input.

       Attributes:
           expression -- input expression in which the error occurred
           message -- explanation of the error
       """

       def __init__(self, expression, message):
           self.expression = expression
           self.message = message

   class TransitionError(Error):
       """Raised when an operation attempts a state transition that's not
       allowed.

       Attributes:
           previous -- state at beginning of transition
           next -- attempted new state
           message -- explanation of why the specific transition is not allowed
       """

       def __init__(self, previous, next, message):
           self.previous = previous
           self.next = next
           self.message = message

Most exceptions are defined with names that end in "Error," similar to the
naming of the standard exceptions.

Many standard modules define their own exceptions to report errors that may
occur in functions they define.  More information on classes is presented in
chapter :ref:`tut-classes`.


.. _tut-cleanup:

Defining Clean-up Actions
=========================

The :keyword:`try` statement has another optional clause which is intended to
define clean-up actions that must be executed under all circumstances.  For
example::

   >>> try:
   ...     raise KeyboardInterrupt
   ... finally:
   ...     print 'Goodbye, world!'
   ...
   Goodbye, world!
   Traceback (most recent call last):
     File "<stdin>", line 2, in ?
   KeyboardInterrupt

A *finally clause* is always executed before leaving the :keyword:`try`
statement, whether an exception has occurred or not. When an exception has
occurred in the :keyword:`try` clause and has not been handled by an
:keyword:`except` clause (or it has occurred in a :keyword:`except` or
:keyword:`else` clause), it is re-raised after the :keyword:`finally` clause has
been executed.  The :keyword:`finally` clause is also executed "on the way out"
when any other clause of the :keyword:`try` statement is left via a
:keyword:`break`, :keyword:`continue` or :keyword:`return` statement.  A more
complicated example (having :keyword:`except` and :keyword:`finally` clauses in
the same :keyword:`try` statement works as of Python 2.5)::

   >>> def divide(x, y):
   ...     try:
   ...         result = x / y
   ...     except ZeroDivisionError:
   ...         print "division by zero!"
   ...     else:
   ...         print "result is", result
   ...     finally:
   ...         print "executing finally clause"
   ...
   >>> divide(2, 1)
   result is 2
   executing finally clause
   >>> divide(2, 0)
   division by zero!
   executing finally clause
   >>> divide("2", "1")
   executing finally clause
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
     File "<stdin>", line 3, in divide
   TypeError: unsupported operand type(s) for /: 'str' and 'str'

As you can see, the :keyword:`finally` clause is executed in any event.  The
:exc:`TypeError` raised by dividing two strings is not handled by the
:keyword:`except` clause and therefore re-raised after the :keyword:`finally`
clauses has been executed.

In real world applications, the :keyword:`finally` clause is useful for
releasing external resources (such as files or network connections), regardless
of whether the use of the resource was successful.


.. _tut-cleanup-with:

Predefined Clean-up Actions
===========================

Some objects define standard clean-up actions to be undertaken when the object
is no longer needed, regardless of whether or not the operation using the object
succeeded or failed. Look at the following example, which tries to open a file
and print its contents to the screen. ::

   for line in open("myfile.txt"):
       print line

The problem with this code is that it leaves the file open for an indeterminate
amount of time after the code has finished executing. This is not an issue in
simple scripts, but can be a problem for larger applications. The
:keyword:`with` statement allows objects like files to be used in a way that
ensures they are always cleaned up promptly and correctly. ::

   with open("myfile.txt") as f:
       for line in f:
           print line

After the statement is executed, the file *f* is always closed, even if a
problem was encountered while processing the lines. Other objects which provide
predefined clean-up actions will indicate this in their documentation.


