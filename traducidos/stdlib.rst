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
   >>> os.getcwd()      # devuelve el directorio de trabajo actual
   'C:\\Python35'
   >>> os.chdir('/server/accesslogs')   # cambia el directorio de trabajo
   >>> os.system('mkdir today')   # ejecuta el comando 'mkdir' en el sistema
   0

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
   'archivo.db'
   >>> shutil.move('/build/executables', 'dir_instalac')
   'dir_instalac'


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
   >>> print(sys.argv)
   ['demo.py', 'uno', 'dos', 'tres']

El módulo :mod:`getopt` procesa *sys.argv* usando las convenciones de la
función de Unix :func:`getopt`.  El módulo :mod:`argparse` provee un
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
   >>> math.cos(math.pi / 4)
   0.70710678118654757
   >>> math.log(1024, 2)
   10.0

El módulo :mod:`random` provee herramientas para realizar selecciones al azar::

   >>> import random
   >>> random.choice(['manzana', 'pera', 'banana'])
   'manzana'
   >>> random.sample(range(100), 10)   # elección sin reemplazo
   [30, 83, 16, 4, 8, 81, 41, 50, 18, 33]
   >>> random.random()    # un float al azar
   0.17970987693706186
   >>> random.randrange(6)    # un entero al azar tomado de range(6)
   4

El módulo :mod:`statistics` calcula propiedades de estadística básica
(la media, mediana, varianza, etc) de datos númericos::

    >>> import statistics
    >>> datos = [2.75, 1.75, 1.25, 0.25, 0.5, 1.25, 3.5]
    >>> statistics.mean(datos)
    1.6071428571428572
    >>> statistics.median(datos)
    1.25
    >>> statistics.variance(datos)
    1.3720238095238095

El proyecto SciPy <http://scipy.org> tiene muchos otros módulos para
cálculos numéricos.


.. _tut-internet-access:

Acceso a Internet
=================

Hay varios módulos para acceder a internet y procesar sus protocolos.  Dos de
los más simples son :mod:`urllib.request` para traer data de URLs y
:mod:`smtplib` para mandar correos::

   >>> with urlopen('http://tycho.usno.navy.mil/cgi-bin/timer.pl') as response:
   ...     for line in response:
   ...         line = line.decode('utf-8')  # Decoding the binary data to text.
   ...         if 'EST' in line or 'EDT' in line:  # look for Eastern Time
   ...             print(line)

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

.. _tut-dates-and-times:

Fechas y tiempos
================

El módulo :mod:`datetime` ofrece clases para manejar fechas y tiempos tanto de
manera simple como compleja.  Aunque soporta aritmética sobre fechas y
tiempos, el foco de la implementación es en la extracción eficiente de partes
para manejarlas o formatear la salida.  El módulo también soporta objetos que
son conscientes de la zona horaria. ::

    >>> # las fechas son fácilmente construidas y formateadas
    >>> from datetime import date
    >>> hoy = date.today()
    >>> hoy
    datetime.date(2009, 7, 19)

    >>> # nos aseguramos de tener la info de localización correcta
    >>> import locale
    >>> locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
    'es_ES.UTF8'
    >>> hoy.strftime("%m-%d-%y. %d %b %Y es %A. hoy es %d de %B.")
    '07-19-09. 19 jul 2009 es domingo. hoy es 19 de julio.'

    >>> # las fechas soportan aritmética de calendario
    >>> nacimiento = date(1964, 7, 31)
    >>> edad = hoy - nacimiento
    >>> edad.days
    14368


.. _tut-data-compression:

Compresión de datos
===================

Los formatos para archivar y comprimir datos se soportan directamente con los
módulos: :mod:`zlib`, :mod:`gzip`, :mod:`bz2`, :mod:`lzma`, :mod:`zipfile`
y :mod:`tarfile`.  ::

    >>> import zlib
    >>> s = b'witch which has which witches wrist watch'
    >>> len(s)
    41
    >>> t = zlib.compress(s)
    >>> len(t)
    37
    >>> zlib.decompress(t)
    b'witch which has which witches wrist watch'
    >>> zlib.crc32(s)
    226805979


.. _tut-performance-measurement:

Medición de rendimiento
=======================

Algunos usuarios de Python desarrollan un profundo interés en saber el
rendimiento relativo de las diferentes soluciones al mismo problema.  Python
provee una herramienta de medición que responde esas preguntas inmediatamente.

Por ejemplo, puede ser tentador usar la característica de empaquetamiento y
desempaquetamiento de las tuplas en lugar de la solución tradicional para
intercambiar argumentos.  El módulo :mod:`timeit` muestra rapidamente una
modesta ventaja de rendimiento::

   >>> from timeit import Timer
   >>> Timer('t=a; a=b; b=t', 'a=1; b=2').timeit()
   0.57535828626024577
   >>> Timer('a,b = b,a', 'a=1; b=2').timeit()
   0.54962537085770791

En contraste con el fino nivel de granularidad del módulo :mod:`timeit`, los
módulos :mod:`profile` y :mod:`pstats` proveen herramientas para identificar
secciones críticas de tiempo en bloques de código más grandes.


.. _tut-quality-control:

Control de calidad
==================

Una forma para desarrollar software de alta calidad es escribir pruebas para
cada función mientras se la desarrolla, y correr esas pruebas frecuentemente
durante el proceso de desarrollo.

El módulo :mod:`doctest` provee una herramienta para revisar un módulo y
validar las pruebas integradas en las cadenas de documentación (o *docstring*)
del programa.  La construcción de las pruebas es tan sencillo como cortar y
pegar una ejecución típica junto con sus resultados en los docstrings.  Esto
mejora la documentación al proveer al usuario un ejemplo y permite que el
módulo :mod:`doctest` se asegure que el código permanece fiel a la
documentación::

   def promedio(valores):
       """Calcula la media aritmética de una lista de números.

       >>> print(promedio([20, 30, 70]))
       40.0
       """
       return sum(valores) / len(valores)

   import doctest
   doctest.testmod()   # valida automáticamente las pruebas integradas

El módulo :mod:`unittest` necesita más esfuerzo que el módulo :mod:`doctest`,
pero permite que se mantenga en un archivo separado un conjunto más comprensivo
de pruebas::

   import unittest

   class TestFuncionesEstadisticas(unittest.TestCase):

       def test_promedio(self):
           self.assertEqual(promedio([20, 30, 70]), 40.0)
           self.assertEqual(round(promedio([1, 5, 7]), 1), 4.3)
           with self.assertRaises(ZeroDivisionError):
              promedio([])
           with self.assertRaises(TypeError):
              promedio(20, 30, 70)

   unittest.main() # llamarlo de la linea de comandos ejecuta todas las pruebas


.. _tut-batteries-included:

Las pilas incluidas
===================

Python tiene una filosofía de "pilas incluidas".  Esto se ve mejor en las
capacidades robustas y sofisticadas de sus paquetes más grandes.  Por ejemplo:

* Los módulos :mod:`xmlrpc.client` y :mod:`xmlrpc.server` hacen que
  implementar llamadas a procedimientos remotos sea una tarea trivial.  A
  pesar de los nombres de los módulos, no se necesita conocimiento directo
  o manejo de XML.

* El paquete :mod:`email` es una biblioteca para manejar mensajes de mail,
  incluyendo MIME y otros mensajes basados en RFC 2822.  Al contrario de
  :mod:`smtplib` y :mod:`poplib` que en realidad envían y reciben mensajes,
  el paquete :mod:`email` tiene un conjunto de herramientas completo para
  construir y decodificar estructuras complejas de mensajes (incluyendo
  adjuntos) y para implementar protocolos de cabecera y codificación de
  Internet.

* El paquete :mod:`json` provee soporte robusto para parsear este
  popular formato de intercambio de datos. El módulo :mod:`csv`
  soporta una lectura y escritura directa de archivos de valores
  separados por coma, comunmente soportados por bases de datos y hojas
  de cálculos. Procesar XML es soportado por los paquetes
  :mod:`xml.etree.ElementTree`, :mod:`xml.dom` y
  :mod:`xml.sax`. Juntos, estos tres módulos y paquetes simplifican
  ampliamente el intercambio de datos entre aplicaciones Python y
  otras herramientas.

* El módulo :mod:`sqlite3` es un wrapper para la librería de base de
  datos SQLite, proveyendo una base de datos persistente que puede ser
  actualizada y accedida utilizando sintaxis SQL ligeramente no
  estándar.

* Se soporta la internacionalización a través de varios módulos, incluyendo
  :mod:`gettext`, :mod:`locale`, y el paquete :mod:`codecs`.
