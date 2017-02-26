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

export PATCH_DIR=`pwd`

# Incluimos el script de virtualenvwrapper (requiere
# python-virtualenvwrapper)
. $VIRTUALENVWRAPPER_SCRIPT

echo "Eliminando el entorno virtual 'python-tutorial'"
rmvirtualenv python-tutorial

echo "Creando el entorno Python"
mkvirtualenv --python python2 python-tutorial

set -e

echo "Instalando pdfrw"
pip install pdfrw

echo "Patcheando pdfrw"
cdvirtualenv
cd lib/python2.7/site-packages/pdfrw
patch -p0 < $PATCH_DIR/pdfrw.diff

cd $PATCH_DIR
echo "Eliminando el respositorio de rst2pdf"
rm -rf rst2pdf
echo "Descargando el repositorio de rst2pdf"
git clone https://github.com/rst2pdf/rst2pdf
cd rst2pdf
git checkout db62c731b4d03f2afaeef9803a03cc59389cae8b
python setup.py develop
patch -p0 < $PATCH_DIR/rst2pdf.diff

echo "Instalando Sphinx"
pip install sphinx==1.1.3
pip install sphinx-bootstrap-theme

echo "Instalando Fabric"
pip install fabric

echo "Instalando BeautifulSoup 4"
pip install bs4

echo "Instalando configparser"
pip install configparser

echo "Instalando feedparser"
pip install feedparser

echo "Instalando pdftk"
sudo apt-get install pdftk

echo "Instalando inkscape"
sudo apt-get install inkscape
