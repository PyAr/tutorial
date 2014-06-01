# Fabric script para "deployar" el tutorial de Python 3 en el servidor
# de PyAr y actualizar la version HTML y PDF online en
# http://docs.python.org.ar/tutorial/

from fabric.api import *

# env.hosts = ['python.org.ar']
# env.shell = '/bin/bash -l -c'
# env.project = '/home/www-pyar/docs.python.org.ar/tutorial/'
env.colorize_errors = True


def deploy_all():
    deploy_html3()
    deploy_pdf3()


def deploy_html3():
    local('rsync -rav ' \
          'traducidos/_build/html/* ' \
          'www-pyar@python.org.ar:/home/www-pyar/docs.python.org.ar/tutorial/3/')


def deploy_pdf3():
    local('rsync -rav ' \
          'traducidos/_build/pdf/TutorialPython.pdf ' \
          'www-pyar@python.org.ar:/home/www-pyar/docs.python.org.ar/tutorial/pdfs/TutorialPython3.pdf')


def create_html():
    local('cd traducidos && make html')


def create_pdf():
    local('cd traducidos && make pdf')

    # FIXME: there is an issue with 'gs' that doesn't allow us to use
    # this command to make the .pdf smaller

    # local('cd traducidos && '
    #       'gs -dCompatibilityLevel=1.4 -dCompressFonts=true -dSubsetFonts=true '
    #       '-dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=output2.pdf '
    #       '-f _build/pdf/TutorialPython.pdf')
