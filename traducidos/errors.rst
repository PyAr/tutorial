.. _tut-errors:

*********************
Errores y excepciones
*********************

Hasta ahora los mensajes de error no habían sido más que mencionados, pero si
probaste los ejemplos probablemente hayas visto algunos.  Hay (al menos) dos
tipos diferentes de errores: *errores de sintaxis* y *excepciones*.


.. _tut-syntaxerrors:

Errores de sintaxis
===================

Los errores de sintaxis, también conocidos como errores de interpretación, son
quizás el tipo de queja más común que tenés cuando todavía estás aprendiendo
Python::

   >>> while True print 'Hola mundo'
   Traceback (most recent call last):
   ...
       while True print 'Hola mundo'
                      ^
   SyntaxError: invalid syntax

El intérprete repite la línea culpable y muestra una pequeña 'flecha'
que apunta al primer lugar donde se detectó el error.  Este es causado por (o
al menos detectado en) el símbolo que *precede* a la flecha: en el ejemplo,
el error se detecta en el :keyword:`print`, ya que faltan dos puntos (``':'``)
antes del mismo.  Se muestran el nombre del archivo y el número de línea para
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

La última línea de los mensajes de error indica qué sucedió.  Las excepciones
vienen de distintos tipos, y el tipo se imprime como parte del mensaje: los
tipos en el ejemplo son: :exc:`ZeroDivisionError`, :exc:`NameError` y
:exc:`TypeError`.  La cadena mostrada como tipo de la excepción es el nombre de
la excepción predefinida que ocurrió.  Esto es verdad para todas las
excepciones predefinidas del intérprete, pero no necesita ser verdad para
excepciones definidas por el usuario (aunque es una convención útil).  Los
nombres de las excepciones estándar son identificadores incorporados al
intérprete (no son palabras clave reservadas).

El resto de la línea provee un detalle basado en el tipo de la excepción y qué
la causó.

La parte anterior del mensaje de error muestra el contexto donde la excepción
sucedió, en la forma de un *trazado del error* listando líneas fuente; sin
embargo, no mostrará líneas leídas desde la entrada estándar.

:ref:`bltin-exceptions` lista las excepciones predefinidas y sus significados.


.. _tut-handling:

Manejando excepciones
=====================

Es posible escribir programas que manejen determinadas excepciones.  Mirá el
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

* Primero, se ejecuta el *bloque try* (el código entre las declaración
  :keyword:`try` y :keyword:`except`).

* Si no ocurre ninguna excepción, el *bloque except* se saltea y termina la
  ejecución de la declaración :keyword:`try`.

* Si ocurre una excepción durante la ejecución del *bloque try*, el resto del
  bloque se saltea.  Luego, si su tipo coincide con la excepción nombrada luego
  de la palabra reservada :keyword:`except`, se ejecuta el *bloque except*,
  y la ejecución continúa luego de la declaración :keyword:`try`.

* Si ocurre una excepción que no coincide con la excepción nombrada en el
  :keyword:`except`, esta se pasa a declaraciones :keyword:`try` de más afuera;
  si no se encuentra nada que la maneje, es una *excepción no manejada*, y la
  ejecución se frena con un mensaje como los mostrados arriba.

Una declaración :keyword:`try` puede tener más de un :keyword:`except`, para
especificar manejadores para distintas excepciones.  A lo sumo un manejador
será ejecutado.  Sólo se manejan excepciones que ocurren en el correspondiente
:keyword:`try`, no en otros manejadores del mismo :keyword:`try`.  Un
:keyword:`except` puede nombrar múltiples excepciones usando paréntesis, por
ejemplo::

   ... except (RuntimeError, TypeError, NameError):
   ...     pass

El último :keyword:`except` puede omitir nombrar qué excepción captura, para
servir como comodín.  Usá esto con extremo cuidado, ya que de esta manera es
fácil ocultar un error real de programación.  También puede usarse para mostrar
un mensaje de error y luego re-generar la excepción (permitiéndole al que
llama, manejar también la excepción)::

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

El uso de :keyword:`else` es mejor que agregar código adicional en el
:keyword:`try` porque evita capturar accidentalmente una excepción que no fue
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
único argumento a la excepción (que puede ser una tupla se necesitan varios
argumentos) y vincularlo al atributo ``message``.  Uno también puede instanciar
una excepción antes de generarla, y agregarle cualquier atributo que se
desee::

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

Los manejadores de excepciones no manejan solamente las excepciones que
ocurren en el *bloque try*, también manejan las excepciones que ocurren
dentro de las funciones que se llaman (inclusive indirectamente) dentro del
*bloque try*.  Por ejemplo::

   >>> def esto_falla():
   ...     x = 1/0
   ...
   >>> try:
   ...     esto_falla()
   ... except ZeroDivisionError as detail:
   ...     print 'Manejando error en tiempo de ejecucion:', detail
   ...
   Manejando error en tiempo de ejecucion: integer division or modulo by zero


.. raw:: pdf

   PageBreak

.. _tut-raising:

Levantando excepciones
======================

La declaración :keyword:`raise` permite al programador forzar a que ocurra
una excepción específica.  Por ejemplo::

   >>> raise NameError('Hola')
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   NameError: Hola

El argumento de :keyword:`raise` es una clase o instancia de excepción a ser
generada.  Hay una sintaxis alternativa que no se usa más, que separa los
argumentos de clase y constructor; lo de arriba podría escribirse como
``raise NameError, 'Hola'``; ya que alguna vez era la única opción, esta forma
es muy usada en códigos viejos.

Si necesitás determinar cuando una excepción fue lanzada pero no querés
manejarla, una forma simplificada de la instrucción :keyword:`raise` te permite
relanzarla::

   >>> try:
   ...     raise NameError('Hola')
   ... except NameError:
   ...     print u'Voló una excepción!'
   ...     raise
   ...
   Voló una excpeción!
   Traceback (most recent call last):
     File "<stdin>", line 2, in ?
   NameError: Hola


.. _tut-userexceptions:

Excepciones definidas por el usuario
====================================

Los programas pueden nombrar sus propias excepciones creando una nueva clase
excepción.  Las excepciones, típicamente, deberán derivar de la clase
:exc:`Exception`, directa o indirectamente.  Por ejemplo::

   >>> class MiError(Exception):
   ...     def __init__(self, valor):
   ...         self.valor = valor
   ...     def __str__(self):
   ...         return repr(self.valor)
   ...
   >>> try:
   ...     raise MiError(2*2)
   ... except MyError as e:
   ...     print u'Ocurrió mi excepción, valor:', e.valor
   ...
   Ocurrió mi excepción, valor: 4
   >>> raise MiError('oops!')
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   __main__.MiError: 'oops!'

En este ejemplo, el método :meth:`__init__` de :class:`Exception` fue
sobrescrito.  El nuevo comportamiento simplemente crea el atributo *valor*.
Esto reemplaza el comportamiento por defecto de crear el atributo *args*.

Las clases de Excepciones pueden ser definidas de la misma forma que cualquier
otra clase, pero usualmente se mantienen simples, a menudo solo ofreciendo un
número de atributos con información sobre el error que leerán los manejadores
de la excepción.  Al crear un módulo que puede lanzar varios errores distintos,
una práctica común es crear una clase base para excepciones definidas en ese
módulo y extenderla para crear clases excepciones específicas para distintas
condiciones de error::

   class Error(Exception):
       """Clase base para excepciones en el modulo."""
       pass

   class EntradaError(Error):
       """Excepcion lanzada por errores en las entradas.

       Atributos:
           expresion -- expresion de entrada en la que ocurre el error
           mensaje -- explicacion del error
       """

       def __init__(self, expresion, mensaje):
           self.expresion = expresion
           self.mensaje = mensaje

   class TransicionError(Error):
       """Lanzada cuando una operacion intenta una transicion de estado no
       permitida.

       Atributos:
           previo -- estado al principio de la transicion
           siguiente -- nuevo estado intentado
           mensaje -- explicacion de porque la transicion no esta permitida
       """
       def __init__(self, previo, siguiente, mensaje):
           self.previo = previo
           self.siguiente = siguiente
           self.mensaje = mensaje

La mayoría de las excepciones son definidas con nombres que terminan en
"Error", similares a los nombres de las excepciones estándar.

Muchos módulos estándar definen sus propias excepciones para reportar errores
que pueden ocurrir en funciones propias. Se puede encontrar más información
sobre clases en el capítulo :ref:`tut-classes`.


.. _tut-cleanup:

Definiendo acciones de limpieza
===============================

La declaración :keyword:`try` tiene otra cláusula opcional que intenta
definir acciones de limpieza que deben ser ejecutadas bajo ciertas
circunstancias. Por ejemplo::

   >>> try:
   ...     raise KeyboardInterrupt
   ... finally:
   ...     print 'Chau, mundo!'
   ...
   Chau, mundo!
   Traceback (most recent call last):
     File "<stdin>", line 2, in ?
   KeyboardInterrupt

Una *cláusula finally* siempre es ejecutada antes de salir de la declaración
:keyword:`try`, ya sea que una excepción haya ocurrido o no.  Cuando ocurre una
excepción en la cláusula :keyword:`try` y no fue manejada por una cláusula
:keyword:`except` (o ocurrió en una cláusula :keyword:`except` o
:keyword:`else`), es relanzada luego de que se ejecuta la cláusula
:keyword:`finally`. :keyword:`finally` es también ejecutada "a la salida"
cuando cualquier otra cláusula de la declaración :keyword:`try` es dejada
via :keyword:`break`, :keyword:`continue` or :keyword:`return`.  Un ejemplo
más complicado (cláusulas :keyword:`except` y :keyword:`finally` en la misma
declaración :keyword:`try`)::

   >>> def dividir(x, y):
   ...     try:
   ...         result = x / y
   ...     except ZeroDivisionError:
   ...         print "¡division por cero!"
   ...     else:
   ...         print "el resultado es", result
   ...     finally:
   ...         print "ejecutando la clausula finally"
   ...
   >>> dividir(2, 1)
   el resultado es 2
   ejecutando la clausula finally
   >>> dividir(2, 0)
   ¡division por cero!
   ejecutando la clausula finally
   >>> divide("2", "1")
   ejecutando la clausula finally
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
     File "<stdin>", line 3, in divide
   TypeError: unsupported operand type(s) for /: 'str' and 'str'

Como podés ver, la cláusula :keyword:`finally` es ejecutada siempre.  La
excepción :exc:`TypeError` lanzada al dividir dos cadenas de texto no es
manejado por la cláusula :keyword:`except` y por lo tanto es relanzada luego
de que se ejecuta la cláusula :keyword:`finally`.

En aplicaciones reales, la cláusula :keyword:`finally` es útil para liberar
recursos externos (como archivos o conexiones de red), sin importar si el
uso del recurso fue exitoso.


.. _tut-cleanup-with:

Acciones predefinidas de limpieza
=================================

Algunos objetos definen acciones de limpieza estándar que llevar a cabo cuando
el objeto no es más necesitado, independientemente de que las operaciones
sobre el objeto hayan sido exitosas o no.  Mirá el siguiente ejemplo, que
intenta abrir un archivo e imprimir su contenido en la pantalla.::

   for linea in open("miarchivo.txt"):
       print linea

El problema con este código es que deja el archivo abierto por un periodo de
tiempo indeterminado luego de que termine de ejecutarse.  Esto no es un
problema en scripts simples, pero puede ser un problema en aplicaciones más
grandes.  La declaración :keyword:`with` permite que objetos como archivos sean
usados de una forma que asegure que siempre se los libera rápido y en forma
correcta. ::

   with open("miarchivo.txt") as f:
       for linea in f:
           print linea

Luego de que la declaración sea ejecutada, el archivo *f* siempre es cerrado,
incluso si se encuentra un problema al procesar las líneas.  Otros objetos que
provean acciones de limpieza predefinidas lo indicarán en su documentación.
