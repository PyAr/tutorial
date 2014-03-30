#!/bin/bash

# Este es un script que sigue los pasos programaticamente del
# documento que se encuentra en traducidos/README.txt

# Se debe ejecutar dentro del directorio dev/ donde se encuentra
# alojado

# Es necesario tener virtualenvwrapper instalado ya que se hace uso de
# 'mkvirtualenv' y 'cdvirtualenv' que crean un virtualenv y hace "cd"
# dentro de nuestro virtualenv respectivamente. De cualquier manera no
# es indispensable, pero esos pasos deberían hacerse a mano de lo
# contrario.

set -e

PACTH_DIR=`pwd`

mkvirtualenv python-tutorial

svn checkout http://rst2pdf.googlecode.com/svn/trunk/ rst2pdf
cd rst2pdf
python setup.py develop
patch -p0 < rst2pdf.diff

pip install sphinx # 1.1.3
pip install sphinx-bootstrap-theme

cdvirtualenv
cd lib/python2.7/site-packages/pdfrw-0.1-py2.7.egg/pdfrw/
cp $PATCH_DIR/pdfrw.diff
patch -p0 < pdfrw.diff
