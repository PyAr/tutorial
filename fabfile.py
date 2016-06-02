# Fabric script para "deployar" el tutorial de Python 3 en el servidor
# de PyAr y actualizar la version HTML y PDF online en
# http://docs.python.org.ar/tutorial/

from bs4 import BeautifulSoup
from fabric.api import env, local
from traducidos.conf import version

# env.hosts = ['python.org.ar']
# env.shell = '/bin/bash -l -c'
# env.project = '/home/www-pyar/docs.python.org.ar/tutorial/'
env.colorize_errors = True


def do_all():
    create_all()
    change_htmlindex_version()
    deploy_all()


def deploy_all():
    deploy_index()
    deploy_html3()
    deploy_pdf3()


def deploy_index():
    local('rsync -rav -e "ssh -l www-pyar -p 22215" '
          'traducidos/web/* '
          'www-pyar@python.org.ar:/home/www-pyar/docs.python.org.ar/tutorial/')


def deploy_html3():
    local('rsync -rav -e "ssh -l www-pyar -p 22215" '
          'traducidos/_build/html/* '
          'www-pyar@python.org.ar:/home/www-pyar/docs.python.org.ar/tutorial/3/')


def deploy_pdf3():
    local('rsync -rav -e "ssh -l www-pyar -p 22215" '
          'traducidos/_build/pdf/TutorialPython.pdf '
          'www-pyar@python.org.ar:/home/www-pyar/docs.python.org.ar/tutorial/pdfs/TutorialPython3.pdf')


def create_all():
    create_html()
    create_pdf()


def create_html():
    local('cd traducidos && make html')


def create_ebook():
    """Build an eBook on ePub format using Sphinx."""
    local('cd traducidos && make epub')


def create_pdf():
    local('cd traducidos && make pdf')

    # This command makes the pdf smaller and fixes a SyntaxError that
    # Firefox reports and does not show it properly. This error does
    # not happen with Evince, for example. We are not really sure how
    # this command works, but it does in some way

    # This command was tested with pdftk 2.01
    local(
        'cd traducidos/_build/pdf && '
        'pdftk TutorialPython.pdf cat output output.pdf && '
        'mv output.pdf TutorialPython.pdf'
    )


def change_htmlindex_version():
    # get version from config file
    index_filename = 'traducidos/web/index.html'
    soup = BeautifulSoup(open(index_filename, 'r').read())
    print('Version anterior: {0} | Version nueva: {1}'.format(
        soup.find('h3').contents[0].strip(),
        version,
    ))
    soup.find('h3').contents[0].replace_with(version)

    with open(index_filename, 'w') as fh:
        html_content = soup.prettify(soup.original_encoding)
        fh.write(html_content)


def update_check_script():
    local('scp dev/check_python_tutorial.py '
          'humitos@elblogdehumitos.com.ar:~/src/check_python_tutorial.py')
