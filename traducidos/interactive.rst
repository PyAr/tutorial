.. _tut-interacting:

*********************************************************
Edición de entrada interactiva y sustitución de historial
*********************************************************

Algunas versiones del intérprete de Python permiten editar la línea de entrada
actual, y sustituir en base al historial, de forma similar a las capacidades
del intérprete de comandos Korn y el GNU bash.  Esto se implementa con la
biblioteca `GNU Readline`_, que soporta varios estilos de edición.  Esta
biblioteca tiene su propia documentación la cuál no vamos a duplicar aquí.

.. _tut-keybindings:

Autocompletado con tab e historial de edición
=============================================

El autocompletado de variables y nombres de módulos es ``activado
automáticamente`` al iniciar el intérprete, por lo tanto la
tecla :kbd:`Tab` invoca la función de autocompletado; ésta mira en los nombres
de sentencia, las variables locales y los nombres de módulos disponibles. Para
expresiones con puntos como ``string.a``, va a evaluar la expresión hasta el
``'.'`` final y entonces sugerir autocompletado para los atributos del objeto
resultante. Nota que esto quizás ejecute código de aplicaciones definidas si un
objeto con un método :meth:`__getattr__` es parte de la expresión. La
configuración por omisión también guarda tu historial en un archivo llamado
:file:`.python_history` en tu directorio de usuario. El historial estará
disponible durante la próxima sesión interactiva del intérprete.


.. _tut-commentary:

Alternativas al intérprete interactivo
======================================

Esta funcionalidad es un paso enorme hacia adelante comparado con versiones
anteriores del interprete; de todos modos, quedan pendientes algunos deseos:
sería bueno que el sangrado correcto se sugiriera en las lineas de
continuación (el parser sabe si se requiere un sangrado a continuación).
El mecanismo de completado podría usar la tabla de símbolos del intérprete.
Un comando para verificar (o incluso sugerir) coincidencia de paréntesis,
comillas, etc. también sería útil.

Un intérprete interactivo mejorado alternativo que está dando vueltas desde
hace rato es IPython_, que ofrece completado por tab, exploración de
objetos, y administración avanzada del historial.  También puede ser
configurado en profundidad, e integrarse en otras aplicaciones.  Otro
entorno interactivo mejorado similar es bpython_.

.. _GNU Readline: https://tiswww.case.edu/php/chet/readline/rltop.html
.. _IPython: https://ipython.scipy.org/
.. _bpython: http://www.bpython-interpreter.org/
