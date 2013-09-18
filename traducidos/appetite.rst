.. _tut-intro:

*******************
Abriendo tu apetito
*******************

Si trabajás mucho con computadoras, eventualmente encontrarás que te gustaría
automatizar alguna tarea.  Por ejemplo, podrías desear realizar una búsqueda
y reemplazo en un gran número de archivos de texto, o renombrar y reorganizar
un montón de archivos con fotos de una manera compleja.  Tal vez quieras
escribir alguna pequeña base de datos personalizada, o una aplicación
especializada con interfaz gráfica, o un juego simple.

Si sos un desarrollador de software profesional, tal vez necesites trabajar
con varias bibliotecas de C/C++/Java pero encuentres que se hace lento el ciclo
usual de escribir/compilar/testear/recompilar.  Tal vez estás escribiendo una
batería de pruebas para una de esas bibliotecas y encuentres que escribir el
código de testeo se hace una tarea tediosa.  O tal vez has escrito un programa
al que le vendría bien un lenguaje de extensión, y no quieres
diseñar/implementar todo un nuevo lenguaje para tu aplicación.

Python es el lenguaje justo para ti.

Podrías escribir un script (o programa) en el interprete de comandos o un
archivo por lotes de Windows para algunas de estas tareas, pero los scripts se
lucen para mover archivos de un lado a otro y para modificar datos de texto,
no para aplicaciones con interfaz de usuario o juegos.  Podrías escribir un
programa en C/C++/Java, pero puede tomar mucho tiempo de desarrollo obtener
al menos un primer borrador del programa.  Python es más fácil de usar, está
disponible para sistemas operativos Windows, Mac OS X y Unix, y te ayudará a
realizar tu tarea más velozmente.

Python es fácil de usar, pero es un lenguaje de programación de verdad,
ofreciendo mucha más estructura y soporte para programas grandes de lo que
pueden ofrecer los scripts de Unix o archivos por lotes.  Por otro lado, Python
ofrece mucho más chequeo de error que C, y siendo un *lenguaje de muy alto
nivel*, tiene tipos de datos de alto nivel incorporados como arreglos de tamaño
flexible y diccionarios.  Debido a sus tipos de datos más generales Python
puede aplicarse a un dominio de problemas mayor que Awk o incluso Perl, y aún
así muchas cosas siguen siendo al menos igual de fácil en Python que en esos
lenguajes.

Python te permite separar tu programa en módulos que pueden reusarse en otros
programas en Python.  Viene con una gran colección de módulos estándar que
puedes usar como base de tus programas, o como ejemplos para empezar a
aprender a programar en Python.  Algunos de estos módulos proveen cosas como
entrada/salida a archivos, llamadas al sistema, sockets, e incluso interfaces
a sistemas de interfaz gráfica de usuario como Tk.

Python es un lenguaje interpretado, lo cual puede ahorrarte mucho tiempo durante
el desarrollo ya que no es necesario compilar ni enlazar.  El intérprete puede
usarse interactivamente, lo que facilita experimentar con características del
lenguaje, escribir programas descartables, o probar funciones cuando se hace
desarrollo de programas de abajo hacia arriba. Es también una calculadora
de escritorio práctica.

Python permite escribir programas compactos y legibles.  Los programas en
Python son típicamente más cortos que sus programas equivalentes en C, C++ o
Java por varios motivos:

* los tipos de datos de alto nivel permiten expresar operaciones complejas en
  una sola instrucción

* la agrupación de instrucciones se hace por sangría en vez de llaves de
  apertura y cierre

* no es necesario declarar variables ni argumentos.

Python es *extensible*: si ya sabes programar en C es fácil agregar una nueva
función o módulo al intérprete, ya sea para realizar operaciones críticas
a velocidad máxima, o para enlazar programas Python con bibliotecas que tal
vez sólo estén disponibles en forma binaria (por ejemplo bibliotecas gráficas
específicas de un fabricante).  Una vez que estés realmente entusiasmado, podés
enlazar el intérprete Python en una aplicación hecha en C y usarlo como lenguaje
de extensión o de comando para esa aplicación.

Por cierto, el lenguaje recibe su nombre del programa de televisión de la BBC
"Monty Python's Flying Circus" y no tiene nada que ver con reptiles.  Hacer
referencias a sketches de Monty Python en la documentación no sólo esta
permitido, ¡sino que también está bien visto!

Ahora que ya estás emocionado con Python, querrás verlo en más detalle.  Como
la mejor forma de aprender un lenguaje es usarlo, el tutorial te invita a que
juegues con el intérprete de Python a medida que vas leyendo.

En el próximo capítulo se explicará la mecánica de uso del intérprete.  Esta es
información bastante mundana, pero es esencial para poder probar los ejemplos
que aparecerán más adelante.

El resto del tutorial introduce varias características del lenguaje y el sistema
Python a través de ejemplos, empezando con expresiones, instrucciones y tipos de
datos simples, pasando por funciones y módulos, y finalmente tocando conceptos
avanzados como excepciones y clases definidas por el usuario.
