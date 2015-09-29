. _tut-venv:

*********************************
Entornos Virtuales y Paquetes
*********************************

Introducción
============

Las aplicaciones en Python usualmente hacen uso de paquetes y módulos 
que no forman parte de las librerías estándar. Las aplicaciones a veces
necesitan una versión específica de una librería, debido a que dicha
aplicación requiere que una debilidad particular haya sido solucionada
o bien la aplicación ha sido escrita usando una versión obsoleta de la
interface de la librería.

Esto significa que tal vez no sea posible para una instalación de Python
cumplir los requerimientos de todas las aplicaciones. Si la aplicación A
necesita la versión 1.0 de un módulo particular y la aplicación B necesita
la versión 2.0, entonces los requerimientos entran en conflicto e instalar
la versión 1.0 o 2.0 dejará una de las aplicaciones sin funcionar.

La solución a este problema es crear un :term:`virtual
environment` (comunmente abreviado como "virtualenv"), una directorio que
contiene una instalación de Python de una versión en particular, además de
unos cuantos paquetes adicionales.

Diferentes aplicaciones pueden entonces usar entornos virtuales diferentes.
Para resolver el ejemplo de requerimientos en conflicto citado anteriormente,
la aplicación A puede tener su propio entorno virtual con la versión 1.0 instalada
mientras que la aplicación B tiene otro entorno virtual  con la versión 2.0.
Si la aplicación B requiere que actualizar la librería a la versión 3.0, ésto no 
afectará el entorno virtual de la aplicación A. 


Creando Entornos Virtuales
=============================

El script usado para crear y manejar entornos virtuales es 
:program:`pyvenv`.  :program:`pyvenv` normalmente instalará la versión
mas reciente de Python que Ud. tenga disponible; el script también se 
instalará con una versión, con lo que si tiene múltiples versiones
de Python en su sistema puede seleccionar una versión de Python específica
ejecutando ``pyvenv-3.4`` o la versión que desee.

Para crear un virtualenv(Entorno Virtual), decida en que carpeta 
quiere crearlo y ejecute :program:`pyvenv con la ruta a la carpeta:

   pyvenv tutorial-env 

Esto creará la carpeta ``tutorial-env`` si no existe, y también creará
las subcarpetas conteniendo la copia del intérprete Python, las librerías
estándar y los archivos de soporte.

Una vez creado el entorno virtual, necesita activarlo.

En Windows, ejecutar::

  tutorial-env/Scripts/activate

En Unix o MacOS, ejecute::

  source tutorial-env/bin/activate

(Este script está escrito para la consola bash. Si Ud. usa las
consolas :program:`csh` or :program:`fish`, hay scripts alternativos
``activate.csh`` and ``activate.fish`` que deberá usar en su lugar)

Activar el entorno virtual cambiará el prompt de su consola para mostrar
que entorno virtual está usando, y modificará el entorno para que al correr
``python`` sea con esa versión e instalación en particular. Por ejemplo:

  -> source ~/envs/tutorial-env/bin/activate
  (tutorial-env) -> python
  Python 3.4.3+ (3.4:c7b9645a6f35+, May 22 2015, 09:31:25)
    ...
  >>> import sys
  >>> sys.path
  ['', '/usr/local/lib/python34.zip', ...,
  '~/envs/tutorial-env/lib/python3.4/site-packages']
  >>>


Manejando paquetes con pip
==========================

Una vez activado un entorno virtual, se puede instalar, actualizar y remover
paquetes usando un programa llamado :program:`pip`. Por defecto ``pip`` instalará
paquetes desde Python Package Index (Indice de Paquetes Python),
<https://pypi.python.org/pypi> . Se puede navegar Python Package Index ingresando
con su navegador de internet, o se puede usar la búsqueda limitada de `pip``'s

  (tutorial-env) -> pip search astronomy
  skyfield               - Elegant astronomy for Python
  gary                   - Galactic astronomy and gravitational dynamics.
  novas                  - The United States Naval Observatory NOVAS astronomy library
  astroobs               - Provides astronomy ephemeris to plan telescope observations
  PyAstronomy            - A collection of astronomy related tools for Python.
  ...


``pip`` tiene varios subcomandos: "search", "install", "uninstall",
"freeze", etc.  (Consultar la guía :ref:`installing-index` para la documentación
completa de ``pip``.)

Se puede instalar la última versión de un paquete especificando el nombre del paquete::

  -> pip install novas
  Collecting novas
    Downloading novas-3.1.1.3.tar.gz (136kB)
  Installing collected packages: novas
    Running setup.py install for novas
  Successfully installed novas-3.1.1.3

También se puede instalar una verisón específica de un paquete ingresando
el nombre del paquete seguido de ``==`` y el número de versión:: 

  -> pip install requests==2.6.0
  Collecting requests==2.6.0
    Using cached requests-2.6.0-py2.py3-none-any.whl
  Installing collected packages: requests
  Successfully installed requests-2.6.0

Si se re-ejecuta el comando, ``pip`` detectará que la versión ya 
está instalada y no hará nada. Se puede ingresar un número de versión
diferente para instalarlo, o se puede ejecutar ``pip install --upgrade``
para actualizar el paquete a la última versión::

  -> pip install --upgrade requests
  Collecting requests
  Installing collected packages: requests
    Found existing installation: requests 2.6.0
      Uninstalling requests-2.6.0:
        Successfully uninstalled requests-2.6.0
  Successfully installed requests-2.7.0

``pip uninstall`` seguido de uno o varios nombres de paquetes desinstalará
los paquetes del entorno virtual.

``pip show`` mostrará información de un paquete en particular::

  (tutorial-env) -> pip show requests
  ---
  Metadata-Version: 2.0
  Name: requests
  Version: 2.7.0
  Summary: Python HTTP for Humans.
  Home-page: http://python-requests.org
  Author: Kenneth Reitz
  Author-email: me@kennethreitz.com
  License: Apache 2.0
  Location: /Users/akuchling/envs/tutorial-env/lib/python3.4/site-packages
  Requires:

``pip list`` mostrará todos los paquetes instalados en el entorno virtual::

  (tutorial-env) -> pip list
  novas (3.1.1.3)
  numpy (1.9.2)
  pip (7.0.3)
  requests (2.7.0)
  setuptools (16.0)

``pip freeze`` devuelve una lista de paquetes instalados similar, pero el
formato de salida es el requerido por ``pip install``.
Una convención común es poner esta lista en un archivo ``requirements.txt``::
  (tutorial-env) -> pip freeze > requirements.txt
  (tutorial-env) -> cat requirements.txt
  novas==3.1.1.3
  numpy==1.9.2
  requests==2.7.0

El archivo ``requirements.txt`` puede entonces ser confirmado para control
de versiones y entregado como parte de una aplicación. Los usuarios pueden
entonces instalar todos los paquetes necesarios con ``install -r``::
  -> pip install -r requirements.txt
  Collecting novas==3.1.1.3 (from -r requirements.txt (line 1))
    ...
  Collecting numpy==1.9.2 (from -r requirements.txt (line 2))
    ...
  Collecting requests==2.7.0 (from -r requirements.txt (line 3))
    ...
  Installing collected packages: novas, numpy, requests
    Running setup.py install for novas
  Successfully installed novas-3.1.1.3 numpy-1.9.2 requests-2.7.0

``pip`` tiene muchas opciones más. Consultar la guía :ref:`installing-index`
para la documentación de ``pip``. Cuando Ud. haya escrito un paquete y desee
dejarlo disponible en Python Package Index, consulte la guía :ref:`distributing-index`.
