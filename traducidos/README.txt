Nos bajamos el trunk de rst2pdf y usamos ese. Estas pruebas están hechas
con la versión 2632.

  svn checkout http://rst2pdf.googlecode.com/svn/trunk/ rst2pdf

No lo instalamos, sino que hacemos...

  sudo python setup.py develop

...con lo que sólo instalamos algo que nos usa el trunk cuando lo
importemos (si actualizamos el proyecto, no lo tenemos que reinstalar).

A esa versión la parcheamos con...

  http://pastebin.ubuntu.com/5572041/

...que nos va a corregir dos cosas:

  - no meter una página en blanco luego de que termine un capítulo que tiene
    notas al pie

  - hacer que nunca un título quede solitario al final de una página

Quizás estos parches luego entren al trunk de rst2pdf, si estás leyendo esto
y ves que eso pasó, rearmar por favor estas instrucciones, :)


La versión de sphinx que usé es la que trae Quantal por default:

  1.1.3+dfsg-4ubuntu3


Una última consideración con respecto a las herramientas utilizadas. Resulta que inkscape genera mal el PDF de los títulos cabecera de capítulo (ver

  https://bugs.launchpad.net/ubuntu/+source/inkscape/+bug/1131731

), así que para que no crashee el que arma todo el PDF, tuve que patchear el
archivo "pdfreader.py" del proyecto "pdfrw" con lo siguiente:

  http://pastebin.ubuntu.com/5573793/


En fin, ya estamos en posición de generar el PDF. Vamos al directorio de 'traducidos'
y hacemos:

  make pdf

Esto nos deja _build/pdf/TutorialPython.pdf

Hay varios tipos de PDFs que podemos generar (hoy por hoy: uno en hoja pequeña, blanco y negro, a dos páginas, para imprimir en imprenta, y otro A4, en color, para leer de la PC o imprimir en casa), esto se controla con el campo "pdf_stylesheets" del conf.py.

Para generar el html:

  make html

Esto nos deja varios archivos en _build/html/

