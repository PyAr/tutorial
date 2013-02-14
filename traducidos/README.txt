Nos bajamos el trunk de rst2pdf y usamos ese. Estas pruebas están hechas
con la versión 2317 (FIXME: 2632).

  svn checkout http://rst2pdf.googlecode.com/svn/trunk/ rst2pdf

No lo instalamos, sino que hacemos...

  sudo python setup.py develop

...con lo que sólo instalamos algo que nos usa el trunk cuando lo
importemos (si actualizamos el proyecto, no lo tenemos que reinstalar).

Luego hacemos exactamente lo mismo con Sphinx, tomando el proyecto de:

  hg clone http://bitbucket.org/birkenfeld/sphinx/

Ya estamos en posición de generar el PDF. Vamos al directorio de 'traducidos'
y hacemos:

  make pdf

Esto nos deja _build/pdf/TutorialPython.pdf

FIXME: hacer una version full color

FIXME: ver el tema de hacer un titulo de ejemplos
