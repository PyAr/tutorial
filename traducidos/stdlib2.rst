.. _tut-brieftourtwo:

*************************************************
Pequeño pase por la Bibliotec Estándar - Parte II
*************************************************

This second tour covers more advanced modules that support professional
programming needs.  These modules rarely occur in small scripts.


.. _tut-output-formatting:

Formato de salida
=================

El módulo :mod:`repr` provee una versión de :func:`repr` personalizada
para mostrar abreviados
The :mod:`repr` module provides a version of :func:`repr` customized for
abbreviated displays of large or deeply nested containers::

   >>> import repr
   >>> repr.repr(set('supercalifragilisticexpialidocious'))
   "set(['a', 'c', 'd', 'e', 'f', 'g', ...])"

The :mod:`pprint` module offers more sophisticated control over printing both
built-in and user defined objects in a way that is readable by the interpreter.
When the result is longer than one line, the "pretty printer" adds line breaks
and indentation to more clearly reveal data structure::

   >>> import pprint
   >>> t = [[[['black', 'cyan'], 'white', ['green', 'red']], [['magenta',
   ...     'yellow'], 'blue']]]
   ...
   >>> pprint.pprint(t, width=30)
   [[[['black', 'cyan'],
      'white',
      ['green', 'red']],
     [['magenta', 'yellow'],
      'blue']]]

The :mod:`textwrap` module formats paragraphs of text to fit a given screen
width::

   >>> import textwrap
   >>> doc = """The wrap() method is just like fill() except that it returns
   ... a list of strings instead of one big string with newlines to separate
   ... the wrapped lines."""
   ...
   >>> print textwrap.fill(doc, width=40)
   The wrap() method is just like fill()
   except that it returns a list of strings
   instead of one big string with newlines
   to separate the wrapped lines.

The :mod:`locale` module accesses a database of culture specific data formats.
The grouping attribute of locale's format function provides a direct way of
formatting numbers with group separators::

   >>> import locale
   >>> locale.setlocale(locale.LC_ALL, 'English_United States.1252')
   'English_United States.1252'
   >>> conv = locale.localeconv()          # get a mapping of conventions
   >>> x = 1234567.8
   >>> locale.format("%d", x, grouping=True)
   '1,234,567'
   >>> locale.format("%s%.*f", (conv['currency_symbol'],
   ...	      conv['frac_digits'], x), grouping=True)
   '$1,234,567.80'


.. _tut-templating:

Templating
==========

The :mod:`string` module includes a versatile :class:`Template` class with a
simplified syntax suitable for editing by end-users.  This allows users to
customize their applications without having to alter the application.

The format uses placeholder names formed by ``$`` with valid Python identifiers
(alphanumeric characters and underscores).  Surrounding the placeholder with
braces allows it to be followed by more alphanumeric letters with no intervening
spaces.  Writing ``$$`` creates a single escaped ``$``::

   >>> from string import Template
   >>> t = Template('${village}folk send $$10 to $cause.')
   >>> t.substitute(village='Nottingham', cause='the ditch fund')
   'Nottinghamfolk send $10 to the ditch fund.'

The :meth:`substitute` method raises a :exc:`KeyError` when a placeholder is not
supplied in a dictionary or a keyword argument. For mail-merge style
applications, user supplied data may be incomplete and the
:meth:`safe_substitute` method may be more appropriate --- it will leave
placeholders unchanged if data is missing::

   >>> t = Template('Return the $item to $owner.')
   >>> d = dict(item='unladen swallow')
   >>> t.substitute(d)
   Traceback (most recent call last):
     . . .
   KeyError: 'owner'
   >>> t.safe_substitute(d)
   'Return the unladen swallow to $owner.'

Template subclasses can specify a custom delimiter.  For example, a batch
renaming utility for a photo browser may elect to use percent signs for
placeholders such as the current date, image sequence number, or file format::

   >>> import time, os.path
   >>> photofiles = ['img_1074.jpg', 'img_1076.jpg', 'img_1077.jpg']
   >>> class BatchRename(Template):
   ...     delimiter = '%'
   >>> fmt = raw_input('Enter rename style (%d-date %n-seqnum %f-format):  ')
   Enter rename style (%d-date %n-seqnum %f-format):  Ashley_%n%f

   >>> t = BatchRename(fmt)
   >>> date = time.strftime('%d%b%y')
   >>> for i, filename in enumerate(photofiles):
   ...     base, ext = os.path.splitext(filename)
   ...     newname = t.substitute(d=date, n=i, f=ext)
   ...     print '{0} --> {1}'.format(filename, newname)

   img_1074.jpg --> Ashley_0.jpg
   img_1076.jpg --> Ashley_1.jpg
   img_1077.jpg --> Ashley_2.jpg

Another application for templating is separating program logic from the details
of multiple output formats.  This makes it possible to substitute custom
templates for XML files, plain text reports, and HTML web reports.


.. _tut-binary-formats:

Working with Binary Data Record Layouts
=======================================

The :mod:`struct` module provides :func:`pack` and :func:`unpack` functions for
working with variable length binary record formats.  The following example shows
how to loop through header information in a ZIP file without using the
:mod:`zipfile` module.  Pack codes ``"H"`` and ``"I"`` represent two and four
byte unsigned numbers respectively.  The ``"<"`` indicates that they are
standard size and in little-endian byte order::

   import struct

   data = open('myfile.zip', 'rb').read()
   start = 0
   for i in range(3):                      # show the first 3 file headers
       start += 14
       fields = struct.unpack('<IIIHH', data[start:start+16])
       crc32, comp_size, uncomp_size, filenamesize, extra_size = fields

       start += 16
       filename = data[start:start+filenamesize]
       start += filenamesize
       extra = data[start:start+extra_size]
       print filename, hex(crc32), comp_size, uncomp_size

       start += extra_size + comp_size     # skip to the next header


.. _tut-multi-threading:

Multi-threading
===============

Threading is a technique for decoupling tasks which are not sequentially
dependent.  Threads can be used to improve the responsiveness of applications
that accept user input while other tasks run in the background.  A related use
case is running I/O in parallel with computations in another thread.

The following code shows how the high level :mod:`threading` module can run
tasks in background while the main program continues to run::

   import threading, zipfile

   class AsyncZip(threading.Thread):
       def __init__(self, infile, outfile):
           threading.Thread.__init__(self)
           self.infile = infile
           self.outfile = outfile
       def run(self):
           f = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
           f.write(self.infile)
           f.close()
           print 'Finished background zip of: ', self.infile

   background = AsyncZip('mydata.txt', 'myarchive.zip')
   background.start()
   print 'The main program continues to run in foreground.'

   background.join()    # Wait for the background task to finish
   print 'Main program waited until background was done.'

The principal challenge of multi-threaded applications is coordinating threads
that share data or other resources.  To that end, the threading module provides
a number of synchronization primitives including locks, events, condition
variables, and semaphores.

While those tools are powerful, minor design errors can result in problems that
are difficult to reproduce.  So, the preferred approach to task coordination is
to concentrate all access to a resource in a single thread and then use the
:mod:`Queue` module to feed that thread with requests from other threads.
Applications using :class:`Queue.Queue` objects for inter-thread communication
and coordination are easier to design, more readable, and more reliable.


.. _tut-logging:

Logging
=======

The :mod:`logging` module offers a full featured and flexible logging system.
At its simplest, log messages are sent to a file or to ``sys.stderr``::

   import logging
   logging.debug('Debugging information')
   logging.info('Informational message')
   logging.warning('Warning:config file %s not found', 'server.conf')
   logging.error('Error occurred')
   logging.critical('Critical error -- shutting down')

This produces the following output::

   WARNING:root:Warning:config file server.conf not found
   ERROR:root:Error occurred
   CRITICAL:root:Critical error -- shutting down

By default, informational and debugging messages are suppressed and the output
is sent to standard error.  Other output options include routing messages
through email, datagrams, sockets, or to an HTTP Server.  New filters can select
different routing based on message priority: :const:`DEBUG`, :const:`INFO`,
:const:`WARNING`, :const:`ERROR`, and :const:`CRITICAL`.

The logging system can be configured directly from Python or can be loaded from
a user editable configuration file for customized logging without altering the
application.


.. _tut-weak-references:

Weak References
===============

Python does automatic memory management (reference counting for most objects and
:term:`garbage collection` to eliminate cycles).  The memory is freed shortly
after the last reference to it has been eliminated.

This approach works fine for most applications but occasionally there is a need
to track objects only as long as they are being used by something else.
Unfortunately, just tracking them creates a reference that makes them permanent.
The :mod:`weakref` module provides tools for tracking objects without creating a
reference.  When the object is no longer needed, it is automatically removed
from a weakref table and a callback is triggered for weakref objects.  Typical
applications include caching objects that are expensive to create::

   >>> import weakref, gc
   >>> class A:
   ...     def __init__(self, value):
   ...             self.value = value
   ...     def __repr__(self):
   ...             return str(self.value)
   ...
   >>> a = A(10)                   # create a reference
   >>> d = weakref.WeakValueDictionary()
   >>> d['primary'] = a            # does not create a reference
   >>> d['primary']                # fetch the object if it is still alive
   10
   >>> del a                       # remove the one reference
   >>> gc.collect()                # run garbage collection right away
   0
   >>> d['primary']                # entry was automatically removed
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
       d['primary']                # entry was automatically removed
     File "C:/python26/lib/weakref.py", line 46, in __getitem__
       o = self.data[key]()
   KeyError: 'primary'


.. _tut-list-tools:

Herramientas para trabajar con listas
=====================================

Muchas necesidades de estructuras de datos pueden ser satisfechas con el tipo
lista integrado. Sin embargo, a veces se hacen necesarias implementaciones
alternativas con rendimientos distintos.

El módulo :mod:`array` provee un objeto :class:`array()` (vector) que es como
una lista que almacena sólo datos homogéneos y de una manera más compacta.  Los
ejemplos a continuación muestran un vector de números guardados como dos
números binarios sin signo de dos bytes (código de tipo ``"H"``) en lugar de
los 16 bytes por elemento habituales en listas de objetos int de python::

   >>> from array import array
   >>> a = array('H', [4000, 10, 700, 22222])
   >>> sum(a)
   26932
   >>> a[1:3]
   array('H', [10, 700])

El módulo :mod:`collections` provee un objeto :class:`deque()` que es como una
lista más rápida para agregar y quitar elementos por el lado izquierdo pero
búsquedas más lentas por el medio. Estos objetos son adecuados para implementar
colas y árboles de búsqueda a lo ancho::

   >>> from collections import deque
   >>> d = deque(["tarea1", "tarea2", "tarea3"])
   >>> d.append("tarea4")
   >>> print "Realizando", d.popleft()
   Realizando tarea1

   no_visitado = deque([nodo_inicial])
   def busqueda_a_lo_ancho(no_visitado):
       nodo = no_visitado.popleft()
       for m in gen_moves(nodo):
           if is_goal(m):
               return m
           no_visitado.append(m)

Además de las implementaciones alternativas de listas, la biblioteca ofrece
otras herramientas como el módulo :mod:`bisect` con funciones para manipular
listas ordenadas::

   >>> import bisect
   >>> puntajes = [(100, 'perl'), (200, 'tcl'), (400, 'lua'), (500, 'python')]
   >>> bisect.insort(puntajes, (300, 'ruby'))
   >>> puntajes
   [(100, 'perl'), (200, 'tcl'), (300, 'ruby'), (400, 'lua'), (500, 'python')]

El módulo :mod:`heapq` provee funciones para implementar heaps basados en
listas comunes. El menor valor ingresado se mantiene en la posición cero.  Esto
es útil para aplicaciones que acceden seguido al elemento más chico pero no
quieren hacer una orden completo de la lista::

   >>> from heapq import heapify, heappop, heappush
   >>> datos = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
   >>> heapify(datos)                      # acomodamos la lista a orden de heap
   >>> heappush(datos, -5)                 # agregamos un elemento
   >>> [heappop(datos) for i in range(3)]  # traemos los tres elementos más chicos
   [-5, 0, 1]


.. _tut-decimal-fp:

Aritmética de punto flotante decimal
====================================

El módulo :mod:`decimal` provee un tipo de dato :class:`Decimal` para soportar
aritmética de punto flotante decimal. Comparado con :class:`float`, la
implementación de punto flotante binario incluida, la nueva clase es muy útil
especialmente para aplicaciones financieras y para cualquier uso que requiera
una representación decimal exacta, control de la precisión, control del
redondeo para satisfacer requerimientos legales o reglamentarios, seguimiento
de cifras significativas, o para aplicaciones donde el usuario espera que los
resultados coincidan con cálculos hechos a mano.

Por ejemplo, calcular un impuesto del 5% de una tarifa telefónica de 70
centavos da resultados distintos con punto flotante decimal y punto flotante
binario. La diferencia se vuelve importante si los resultados se redondean al
centavo más próximo::

   >>> from decimal import *
   >>> Decimal('0.70') * Decimal('1.05')
   Decimal("0.7350")
   >>> .70 * 1.05
   0.73499999999999999

El resultado con :class:`Decimal` conserva un cero al final, calculando
automáticamente cuatro cifras significativas a partir de los multiplicandos con
dos cifras significativas.  Decimal reproduce la matemática como se la hace a
mano, y evita problemas que pueden surgir cuando el punto flotante binario no
puede representar exactamente cantidades decimales.

La representación exacta permite a la clase :class:`Decimal` hacer cálculos de
modulo y pruebas de igualdad que son inadecuadas para punto flotante binario::

   >>> Decimal('1.00') % Decimal('.10')
   Decimal("0.00")
   >>> 1.00 % 0.10
   0.09999999999999995

   >>> sum([Decimal('0.1')]*10) == Decimal('1.0')
   True
   >>> sum([0.1]*10) == 1.0
   False

El módulo :mod:`decimal` provee aritmética con tanta precisión como haga falta::

   >>> getcontext().prec = 36
   >>> Decimal(1) / Decimal(7)
   Decimal("0.142857142857142857142857142857142857")


