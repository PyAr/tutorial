.. _tut-brieftourtwo:

***************************************************
Pequeño paseo por la Biblioteca Estándar - Parte II
***************************************************

Este segundo paseo cubre módulos más avanzados que facilitan necesidades
de programación complejas.  Estos módulos raramente se usan en scripts cortos.


.. _tut-output-formatting:

Formato de salida
=================

El módulo :mod:`reprlib` provee una versión de :func:`repr` ajustada para
mostrar contenedores grandes o profundamente anidados, en forma abreviada:

   >>> import reprlib
   >>> reprlib.repr(set('supercalifragilisticoespialidoso'))
   "{'a', 'c', 'd', 'e', 'f', 'g', ...}"

El módulo :mod:`pprint` ofrece un control más sofisticado de la forma
en que se imprimen tanto los objetos predefinidos como los objetos
definidos por el usuario, de manera que sean legibles por el intérprete.
Cuando el resultado ocupa más de una línea, el generador de
"impresiones lindas" agrega saltos de línea y sangrías para mostrar
la estructura de los datos más claramente::

   >>> import pprint
   >>> t = [[[['negro', 'turquesa'], 'blanco', ['verde', 'rojo']], [['magenta',
   ...     'amarillo'], 'azul']]]
   ...
   >>> pprint.pprint(t, width=30)
   [[[['negro', 'turquesa'],
      'blanco',
      ['verde', 'rojo']],
     [['magenta', 'amarillo'],
      'azul']]]

El módulo :mod:`textwrap` formatea párrafos de texto para que quepan
dentro de cierto ancho de pantalla::

   >>> import textwrap
   >>> doc = """El método wrap() es como fill(), excepto que devuelve
   ... una lista de strings en lugar de una gran string con saltos de
   ... línea como separadores."""
   >>> print(textwrap.fill(doc, width=40))
   El método wrap() es como fill(), excepto
   que devuelve una lista de strings en
   lugar de una gran string con saltos de
   línea como separadores.

El módulo :mod:`locale` accede a una base de datos de formatos específicos
a una cultura.  El atributo `grouping` de la función :func:`format`
permite una forma directa de formatear números con separadores de grupo::

   >>> import locale
   >>> locale.setlocale(locale.LC_ALL, '')
   'Spanish_Argentina.1252'
   >>> conv = locale.localeconv()      # obtener un mapeo de convenciones
   >>> x = 1234567.8
   >>> locale.format("%d", x, grouping=True)
   '1.234.567'
   >>> locale.format_string("%s%.*f", (conv['currency_symbol'],
   ...	                    conv['frac_digits'], x), grouping=True)
   '$1.234.567,80'


.. _tut-templating:

Plantillas
==========

El módulo :mod:`string` incluye una clase versátil
:class:`~string.Template` (plantilla) con una sintaxis simplificada
apta para ser editada por usuarios finales.  Esto permite que los
usuarios personalicen sus aplicaciones sin necesidad de modificar la
aplicación en sí.

El formato usa marcadores cuyos nombres se forman con ``$`` seguido de
identificadores Python válidos (caracteres alfanuméricos y guión de subrayado).
Si se los encierra entre llaves, pueden seguir más caracteres alfanuméricos
sin necesidad de dejar espacios en blanco. ``$$`` genera un ``$``::

   >>> from string import Template
   >>> t = Template('${village}folk send $$10 to $cause.')
   >>> t.substitute(village='Nottingham', cause='the ditch fund')
   'Nottinghamfolk send $10 to the ditch fund.'

El método :meth:`~string.Temaplte.substitute` lanza :exc:`KeyError`
cuando no se suministra ningún valor para un marcador mediante un
diccionario o argumento por nombre.  Para algunas aplicaciones los
datos suministrados por el usuario puede ser incompletos, y el método
:meth:`~string.Template.safe_substitute` puede ser más apropiado: deja
los marcadores inalterados cuando hay datos faltantes::

   >>> t = Template('Return the $item to $owner.')
   >>> d = dict(item='unladen swallow')
   >>> t.substitute(d)
   Traceback (most recent call last):
     ...
   KeyError: 'owner'
   >>> t.safe_substitute(d)
   'Return the unladen swallow to $owner.'

Las subclases de Template pueden especificar un delimitador propio.
Por ejemplo, una utilidad de renombrado por lotes para un visualizador
de fotos puede escoger usar signos de porcentaje para los marcadores
tales como la fecha actual, el número de secuencia de la imagen,
o el formato de archivo::

   >>> import time, os.path
   >>> photofiles = ['img_1074.jpg', 'img_1076.jpg', 'img_1077.jpg']
   >>> class BatchRename(Template):
   ...     delimiter = '%'
   ...
   >>> fmt = input('Enter rename style (%d-date %n-seqnum %f-format):  ')
   Enter rename style (%d-date %n-seqnum %f-format):  Ashley_%n%f

   >>> t = BatchRename(fmt)
   >>> date = time.strftime('%d%b%y')
   >>> for i, filename in enumerate(photofiles):
   ...     base, ext = os.path.splitext(filename)
   ...     newname = t.substitute(d=date, n=i, f=ext)
   ...     print('{0} --> {1}'.format(filename, newname))

   img_1074.jpg --> Ashley_0.jpg
   img_1076.jpg --> Ashley_1.jpg
   img_1077.jpg --> Ashley_2.jpg

Las plantillas también pueden ser usadas para separar la lógica del programa
de los detalles de múltiples formatos de salida.  Esto permite sustituir
plantillas específicas para archivos XML, reportes en texto plano,
y reportes web en HTML.


.. _tut-binary-formats:

Trabajar con registros estructurados conteniendo datos binarios
===============================================================

El módulo :mod:`struct` provee las funciones :func:`~struct.pack` y
:func:`~struct.unpack` para trabajar con formatos de registros
binarios de longitud variable.  El siguiente ejemplo muestra cómo
recorrer la información de encabezado en un archivo ZIP sin usar el
módulo :mod:`zipfile`.  Los códigos ``"H"`` e ``"I"`` representan
números sin signo de dos y cuatro bytes respectivamente.  El ``"<"``
indica que son de tamaño estándar y los bytes tienen ordenamiento
`little-endian`::

   import struct

   with open('miarchivo.zip', 'rb') as f:
       datos = f.read()

   inicio = 0
   for i in range(3):                     # mostrar los 3 primeros encabezados
       inicio += 14
       campos = struct.unpack('<IIIHH', datos[inicio:inicio+16])
       crc32, tam_comp, tam_descomp, tam_nomarch, tam_extra = fields

       inicio += 16
       nomarch = datos[inicio:inicio+tam_nomarch]
       inicio += tam_nomarch
       extra = datos[inicio:inicio+tam_extra]
       print(nomarch, hex(crc32), tam_comp, tam_descomp)

       inicio += tam_extra + tam_comp     # saltear hasta el próximo encabezado


.. _tut-multi-threading:

Multi-hilos
===========

La técnica de multi-hilos (o multi-threading) permite desacoplar tareas que no
tienen dependencia secuencial.  Los hilos se pueden usar para mejorar el
grado de reacción de las aplicaciones que aceptan entradas del usuario
mientras otras tareas se ejecutan en segundo plano.  Un caso de uso
relacionado es ejecutar E/S en paralelo con cálculos en otro hilo.

El código siguiente muestra cómo el módulo de alto nivel :mod:`threading`
puede ejecutar tareas en segundo plano mientras el programa principal continúa
su ejecución::

   import threading, zipfile

   class AsyncZip(threading.Thread):
       def __init__(self, arch_ent, arch_sal):
           threading.Thread.__init__(self)
           self.arch_ent = arch_ent
           self.arch_sal = arch_sal

       def run(self):
           f = zipfile.ZipFile(self.arch_sal, 'w', zipfile.ZIP_DEFLATED)
           f.write(self.arch_ent)
           f.close()
           print('Terminó zip en segundo plano de: ', self.arch_ent)

   seg_plano = AsyncZip('misdatos.txt', 'miarchivo.zip')
   seg_plano.start()
   print('El programa principal continúa la ejecución en primer plano.')

   seg_plano.join()    # esperar que termine la tarea en segundo plano
   print('El programa principal esperó hasta que el segundo plano terminara.')


El desafío principal de las aplicaciones multi-hilo es la coordinación entre
los hilos que comparten datos u otros recursos.  A ese fin, el módulo threading
provee una serie de primitivas de sincronización que incluyen locks, eventos,
variables de condición, y semáforos.

Aún cuando esas herramientas son poderosas, pequeños errores de diseño pueden
resultar en problemas difíciles de reproducir.  La forma preferida de coordinar
tareas es concentrar todos los accesos a un recurso en un único hilo y después
usar el módulo :mod:`queue` para alimentar dicho hilo con pedidos desde otros
hilos.  Las aplicaciones que usan objetos :class:`~queue.Queue` para
comunicación y coordinación entre hilos son más fáciles de diseñar,
más legibles, y más confiables.


.. _tut-logging:

Registrando
===========

El módulo :mod:`logging` ofrece un sistema de registros (logs) completo y
flexible.  En su forma más simple, los mensajes de registro se envían a un
archivo o a ``sys.stderr``::

   import logging
   logging.debug('Información de depuración')
   logging.info('Mensaje informativo')
   logging.warning('Atención: archivo de configuración %s no se encuentra',
                   'server.conf')
   logging.error('Ocurrió un error')
   logging.critical('Error crítico -- cerrando')

Ésta es la salida obtenida::

.. code-block:: none

   WARNING:root:Atención: archivo de configuración server.conf no se encuentra
   ERROR:root:Ocurrió un error
   CRITICAL:root:Error crítico -- cerrando

De forma predeterminada, los mensajes de depuración e informativos se
suprimen, y la salida se envía al error estándar.  Otras opciones de
salida incluyen mensajes de ruteo a través de correo electrónico,
datagramas, sockets, o un servidor HTTP.  Nuevos filtros pueden
seleccionar diferentes rutas basadas en la prioridad del mensaje:
:const:`~logging.DEBUG`, :const:`~logging.INFO`,
:const:`~logging.WARNING`, :const:`~logging.ERROR`, and
:const:`~logging.CRITICAL` (Depuración, Informativo, Atención, Error y
Crítico respectivamente)

El sistema de registro puede configurarse directamente desde Python
o puede cargarse la configuración desde un archivo editable por el usuario
para personalizar el registro sin alterar la aplicación.


.. _tut-weak-references:

Referencias débiles
===================

Python realiza administración de memoria automática (cuenta de referencias
para la mayoría de los objetos, y `garbage collection` (recolección
de basura) para eliminar ciclos).  La memoria se libera poco después de que
la última referencia a la misma haya sido eliminada.

Esta estrategia funciona bien para la mayoría de las aplicaciones, pero
ocasionalmente aparece la necesidad de hacer un seguimiento de objetos sólo
mientras están siendo usados por alguien más.  Desafortunadamente, el sólo
hecho de seguirlos crea una referencia que los hace permanentes.

El módulo :mod:`weakref` provee herramientas para seguimiento de objetos que
no crean una referencia.  Cuando el objeto no se necesita más, es eliminado
automáticamente de una tabla de referencias débiles y se dispara una
retrollamada (`callback`).  Comúnmente se usa para mantener una `cache` de
objetos que son caros de crear::

   >>> import weakref, gc
   >>> class A:
   ...     def __init__(self, valor):
   ...         self.valor = valor
   ...     def __repr__(self):
   ...         return str(self.valor)
   ...
   >>> a = A(10)                   # crear una referencia
   >>> d = weakref.WeakValueDictionary()
   >>> d['primaria'] = a            # no crea una referencia
   >>> d['primaria']                # traer el objeto si aún está vivo
   10
   >>> del a                       # eliminar la única referencia
   >>> gc.collect()                # recolección de basura justo ahora
   0
   >>> d['primaria']                # la entrada fue automáticamente eliminada
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
       d['primaria']                # la entrada fue automáticamente eliminada
     File "C:/python36/lib/weakref.py", line 46, in __getitem__
       o = self.data[key]()
   KeyError: 'primaria'


.. _tut-list-tools:

Herramientas para trabajar con listas
=====================================

Muchas necesidades de estructuras de datos pueden ser satisfechas con el tipo
integrado lista.  Sin embargo, a veces se hacen necesarias implementaciones
alternativas con rendimientos distintos.

El módulo :mod:`array` provee un objeto :class:`~array.array()`
(vector) que es como una lista que almacena sólo datos homogéneos y de
una manera más compacta.  Los ejemplos a continuación muestran un
vector de números guardados como dos números binarios sin signo de dos
bytes (código de tipo ``"H"``) en lugar de los 16 bytes por elemento
habituales en listas de objetos int de Python::

   >>> from array import array
   >>> a = array('H', [4000, 10, 700, 22222])
   >>> sum(a)
   26932
   >>> a[1:3]
   array('H', [10, 700])

El módulo :mod:`collections` provee un objeto
:class:`~collections.deque()` que es como una lista más rápida para
agregar y quitar elementos por el lado izquierdo pero con búsquedas
más lentas por el medio.  Estos objetos son adecuados para implementar
colas y árboles de búsqueda a lo ancho::

   >>> from collections import deque
   >>> d = deque(["tarea1", "tarea2", "tarea3"])
   >>> d.append("tarea4")
   >>> print("Realizando", d.popleft())
   Realizando tarea1

::

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
listas comunes.  El menor valor ingresado se mantiene en la posición cero.
Esto es útil para aplicaciones que acceden a menudo al elemento más chico pero
no quieren hacer un orden completo de la lista::

   >>> from heapq import heapify, heappop, heappush
   >>> datos = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
   >>> heapify(datos)                     # acomodamos la lista a orden de heap
   >>> heappush(datos, -5)                # agregamos un elemento
   >>> [heappop(datos) for i in range(3)] # traemos los tres elementos menores
   [-5, 0, 1]


.. _tut-decimal-fp:

Aritmética de punto flotante decimal
====================================

El módulo :mod:`decimal` provee un tipo de dato
:class:`~decimal.Decimal` para soportar aritmética de punto flotante
decimal.  Comparado con :class:`float`, la implementación de punto
flotante binario incluida, la clase es muy útil especialmente para:

* aplicaciones financieras y para cualquier uso que requiera una
  representación decimal exacta,
* control de la precisión,
* control del redondeo para satisfacer requerimientos legales o reglamentarios,
* seguimiento de cifras significativas,
* o para aplicaciones donde el usuario espera que los resultados coincidan
  con cálculos hechos a mano.

Por ejemplo, calcular un impuesto del 5% de una tarifa telefónica de 70
centavos da resultados distintos con punto flotante decimal y punto flotante
binario. La diferencia se vuelve significativa si los resultados se redondean
al centavo más próximo::

   >>> from decimal import *
   >>> round(Decimal('0.70') * Decimal('1.05'), 2)
   Decimal('0.74')
   >>> round(0.70 * 1.05, 2)
   0.73

El resultado con :class:`~decimal.Decimal` conserva un cero al final,
calculando automáticamente cuatro cifras significativas a partir de
los multiplicandos con dos cifras significativas.  Decimal reproduce
la matemática como se la hace a mano, y evita problemas que pueden
surgir cuando el punto flotante binario no puede representar
exactamente cantidades decimales.

La representación exacta permite a la clase :class:`~decimal.Decimal`
hacer cálculos de modulo y pruebas de igualdad que son inadecuadas
para punto flotante binario::

   >>> Decimal('1.00') % Decimal('.10')
   Decimal('0.00')
   >>> 1.00 % 0.10
   0.09999999999999995

   >>> sum([Decimal('0.1')]*10) == Decimal('1.0')
   True
   >>> sum([0.1]*10) == 1.0
   False

El módulo :mod:`decimal` provee aritmética con tanta precisión como
haga falta::

   >>> getcontext().prec = 36
   >>> Decimal(1) / Decimal(7)
   Decimal('0.142857142857142857142857142857142857')

