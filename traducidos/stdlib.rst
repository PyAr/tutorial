.. _tut-brieftour:

****************************************
Pequeño paseo por la Biblioteca Estándar
****************************************


.. _tut-os-interface:

Interfaz al sistema operativo
=============================

El módulo :mod:`os` provee docenas de funciones para interactuar
con el sistema operativo::

   >>> import os
   >>> os.system('time 0:02')
   0
   >>> os.getcwd()      # devuelve el directorio de trabajo actual
   'C:\\Python26'
   >>> os.chdir('/server/accesslogs')

Asegurate de usar el estilo ``import os`` en lugar de ``from os import *``.
Esto evitará que :func:`os.open` oculte a la función integrada :func:`open`,
que trabaja bastante diferente.

.. index:: builtin: help

Las funciones integradas :func:`dir` y :func:`help` son útiles como ayudas
interactivas para trabajar con módulos grandes como :mod:`os`::

   >>> import os
   >>> dir(os)
   <devuelve una lista de todas las funciones del módulo>
   >>> help(os)
   <devuelve un manual creado a partir de las documentaciones del módulo>

Para tareas diarias de administración de archivos y directorios, el módulo
:mod:`shutil` provee una interfaz de más alto nivel que es más fácil de usar::

   >>> import shutil
   >>> shutil.copyfile('datos.db', 'archivo.db')
   >>> shutil.move('/build/executables', 'dir_instalac')


.. _tut-file-wildcards:

Comodines de archivos
=====================

El módulo :mod:`glob` provee una función para hacer listas de archivos a partir
de búsquedas con comodines en directorios::

   >>> import glob
   >>> glob.glob('*.py')
   ['primes.py', 'random.py', 'quote.py']


.. _tut-command-line-arguments:

Argumentos de linea de órdenes
==============================

Los programas frecuentemente necesitan procesar argumentos de linea de órdenes.
Estos argumentos se almacenan en el atributo *argv* del módulo :mod:`sys` como
una lista.  Por ejemplo, la siguiente salida resulta de ejecutar
``python demo.py uno dos tres`` en la línea de órdenes::

   >>> import sys
   >>> print sys.argv
   ['demo.py', 'uno', 'dos', 'tres']

El módulo :mod:`getopt` procesa *sys.argv* usando las convenciones de la
función de Unix :func:`getopt`.  El módulo :mod:`optparse` provee un
procesamiento más flexible de la linea de órdenes.


.. _tut-stderr:

Redirección de la salida de error y finalización del programa
=============================================================

El módulo :mod:`sys` también tiene atributos para *stdin*, *stdout*, y
*stderr*.  Este último es útil para emitir mensajes de alerta y error para
que se vean incluso cuando se haya redireccionado *stdout*::

   >>> sys.stderr.write('Alerta, archivo de log no encontrado\n')
   Alerta, archivo de log no encontrado

La forma más directa de terminar un programa es usar ``sys.exit()``.


.. _tut-string-pattern-matching:


Coincidencia en patrones de cadenas
===================================

El módulo :mod:`re` provee herramientas de expresiones regulares para un
procesamiento avanzado de cadenas.  Para manipulación y coincidencias
complejas, las expresiones regulares ofrecen soluciones concisas y
optimizadas::

   >>> import re
   >>> re.findall(r'\bt[a-z]*', 'tres felices tigres comen trigo')
   ['tres', 'tigres', 'trigo']
   >>> re.sub(r'(\b[a-z]+) \1', r'\1', 'gato en el el sombrero')
   'gato en el sombrero'

Cuando se necesita algo más sencillo solamente, se prefieren los métodos de
las cadenas porque son más fáciles de leer y depurar.

   >>> 'te para tos'.replace('tos', 'dos')
   'te para dos'


.. _tut-mathematics:

Matemática
==========

El módulo :mod:`math` permite el acceso a las funciones de la biblioteca C
subyacente para la matemática de punto flotante::

   >>> import math
   >>> math.cos(math.pi / 4.0)
   0.70710678118654757
   >>> math.log(1024, 2)
   10.0

El módulo :mod:`random` provee herramientas para realizar selecciones al azar::

   >>> import random
   >>> random.choice(['manzana', 'pera', 'banana'])
   'manzana'
   >>> random.sample(xrange(100), 10)   # elección sin reemplazo
   [30, 83, 16, 4, 8, 81, 41, 50, 18, 33]
   >>> random.random()    # un float al azar
   0.17970987693706186
   >>> random.randrange(6)    # un entero al azar tomado de range(6)
   4


.. _tut-internet-access:

Acceso a Internet
=================

Hay varios módulos para acceder a internet y procesar sus protocolos.  Dos de
los más simples son :mod:`urllib2` para traer data de URLs y :mod:`smtplib`
para mandar correos::

   >>> import urllib2
   >>> for line in urllib2.urlopen('http://tycho.usno.navy.mil/cgi-bin/timer.pl'):
   ...     if 'EST' in line or 'EDT' in line:  # buscamos la hora del este
   ...         print line

   <BR>Nov. 25, 09:43:32 PM EST

   >>> import smtplib
   >>> server = smtplib.SMTP('localhost')
   >>> server.sendmail('soothsayer@ejemplo.org', 'jcaesar@ejemplo.org',
   ... """To: jcaesar@ejemplo.org
   ... From: soothsayer@ejemplo.org
   ...
   ... Ojo al piojo.
   ... """)
   >>> server.quit()

(Notá que el segundo ejemplo necesita un servidor de correo corriendo en la
máquina local)

------------------- revisado hasta acá!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
.. _tut-dates-and-times:

Fechas y tiempos
================

El módulo :mod:`datetime` ofrece clases para manejar fechas y tiempos tanto de
manera simple como compleja.  Aunque se soporta aritmética sobre fechas y
tiempos, el foco de la implementación es en la eficiente extracción de partes
para manejarlas o formatear la salida.  El módulo también soporta objetos que
son conscientes de la zona horaria. ::

    # las fechas son fácilmente construidas y formateadas
    >>> from datetime import date
    >>> hoy = date.today()
    >>> hoy
    datetime.date(2009, 7, 19)

    # nos aseguramos de tener la info de localización correcta
    >>> locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
    'es_ES.UTF8'
    >>> hoy.strftime("%m-%d-%y. %d %b %Y es %A. hoy es %d de %B.")
    '07-19-09. 19 jul 2009 es domingo. hoy es 19 de julio.'

    # las fechas soportan aritmética de calendario
    >>> nacimiento = date(1964, 7, 31)
    >>> edad = hoy - nacimiento
    >>> edad.days
    14368


.. _tut-data-compression:

Compresión de datos
===================

Los formatos para archivar y comprimir datos se soportan directamente con los
módulos: :mod:`zlib`, :mod:`gzip`, :mod:`bz2`, :mod:`zipfile` y :mod:`tarfile`.
::

    >>> import zlib
    >>> s = 'witch which has which witches wrist watch'
    >>> len(s)
    41
    >>> t = zlib.compress(s)
    >>> len(t)
    37
    >>> zlib.decompress(t)
    'witch which has which witches wrist watch'
    >>> zlib.crc32(s)
    226805979


.. _tut-performance-measurement:

Performance Measurement
=======================

Some Python users develop a deep interest in knowing the relative performance of
different approaches to the same problem. Python provides a measurement tool
that answers those questions immediately.

For ejemplo, it may be tempting to use the tuple packing and unpacking feature
instead of the traditional approach to swapping arguments. The :mod:`timeit`
module quickly demonstrates a modest performance advantage::

   >>> from timeit import Timer
   >>> Timer('t=a; a=b; b=t', 'a=1; b=2').timeit()
   0.57535828626024577
   >>> Timer('a,b = b,a', 'a=1; b=2').timeit()
   0.54962537085770791

In contrast to :mod:`timeit`'s fine level of granularity, the :mod:`profile` and
:mod:`pstats` modules provide tools for identifying time critical sections in
larger blocks of code.


.. _tut-quality-control:

Quality Control
===============

One approach for developing high quality software is to write tests for each
function as it is developed and to run those tests frequently during the
development process.

The :mod:`doctest` module provides a tool for scanning a module and validating
tests embedded in a program's docstrings.  Test construction is as simple as
cutting-and-pasting a typical call along with its results into the docstring.
This improves the documentation by providing the user with an ejemplo and it
allows the doctest module to make sure the code remains true to the
documentation::

   def average(values):
       """Computes the arithmetic mean of a list of numbers.

       >>> print average([20, 30, 70])
       40.0
       """
       return sum(values, 0.0) / len(values)

   import doctest
   doctest.testmod()   # automatically validate the embedded tests

The :mod:`unittest` module is not as effortless as the :mod:`doctest` module,
but it allows a more comprehensive set of tests to be maintained in a separate
file::

   import unittest

   class TestStatisticalFunctions(unittest.TestCase):

       def test_average(self):
           self.assertEqual(average([20, 30, 70]), 40.0)
           self.assertEqual(round(average([1, 5, 7]), 1), 4.3)
           self.assertRaises(ZeroDivisionError, average, [])
           self.assertRaises(TypeError, average, 20, 30, 70)

   unittest.main() # Calling from the command line invokes all tests


.. _tut-batteries-included:

Batteries Included
==================

Python has a "batteries included" philosophy.  This is best seen through the
sophisticated and robust capabilities of its larger packages. For ejemplo:

* The :mod:`xmlrpclib` and :mod:`SimpleXMLRPCServer` modules make implementing
  remote procedure calls into an almost trivial task.  Despite the modules
  names, no direct knowledge or handling of XML is needed.

* The :mod:`email` package is a library for managing email messages, including
  MIME and other RFC 2822-based message documents. Unlike :mod:`smtplib` and
  :mod:`poplib` which actually send and receive messages, the email package has
  a complete toolset for building or decoding complex message structures
  (including attachments) and for implementing internet encoding and header
  protocols.

* The :mod:`xml.dom` and :mod:`xml.sax` packages provide robust support for
  parsing this popular data interchange format. Likewise, the :mod:`csv` module
  supports direct reads and writes in a common database format. Together, these
  modules and packages greatly simplify data interchange between python
  applications and other tools.

* Internationalization is supported by a number of modules including
  :mod:`gettext`, :mod:`locale`, and the :mod:`codecs` package.


